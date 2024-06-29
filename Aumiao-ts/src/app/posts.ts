import { App } from "../app.js";
import { CodeMaoClient } from "../client/CodeMaoClient.js";
import { CommunityScraper } from "../client/scrape/community.js";
import { Community } from "../client/store/sqlite/community.js";
import { Database } from "../client/store/sqlite/db.js";
import { CommunityAPI } from "../types/api.js";
import { FallTask, Rejected, TaskPool, resolve, writeJSONToCSV } from "../utils.js";

export default async function main(app: App) {
    const dbFile = app.envConfig.CODEMAO_DB_FILE || await app.UI.input("请输入数据库位置(输入以.sqlite为结尾的文件路径将创建一个数据库)");
    app.Logger.info(`数据库位置: ${dbFile}`);

    const db = await initDB(app, dbFile);
    if (Rejected.isRejected(db)) {
        app.Logger.error(`数据库初始化失败: ${db.toString()}`);
        return;
    }
    app.Logger.info("数据库初始化成功");

    const selected = await app.UI.selectByObject("请选择操作", {
        "爬取帖子": () => scrapePosts(app, db),
        "查找帖子": () => findPost(app, db),
        "导出帖子": () => exportPosts(app, db),
    });

    try {
        await selected();
    } catch (error: any) {
        app.Logger.error(`操作失败: ${error.toString()}`);
        db.close();
        return;
    }
    db.close();
}

async function findPost(app: App, db: Database) {
    const comDB = new Community(app, db);
    
    await comDB.sync();

    const target = await (await app.UI.selectByObject("请选择查找方式", {
        "匹配标题": async () => comDB.matchByTitle(await app.UI.input("标题: ")),
        "匹配正文": async () => comDB.matchByContent(await app.UI.input("正文: ")),
    }))();

    if (Rejected.isRejected(target)) {
        app.Logger.error(`查找失败: ${target.toString()}`);
        return;
    }
    if (target.length <= 0) {
        app.Logger.info("没有找到任何帖子");
        return;
    }
    await showPost(app, db, target[0].id);
}

async function showPost(app: App, db: Database, id: string) {
    const comDB = new Community(app, db);
    let fall = new FallTask(app);

    await comDB.sync();

    fall.start(`获取ID为 ${app.UI.color.yellow(id)} 的帖子`);

    let rawPost = await fall.waitForLoading<CommunityAPI.PostDetails | null>(async (resolve, reject) => {
        let post = await comDB.getPostById(id);
        if (Rejected.isRejected(post)) {
            reject(post.toString());
            return null;
        }
        resolve("");
        return post;
    }, "正在获取…");

    if (!rawPost) {
        fall.end(app.UI.color.red("获取失败"));
        return;
    }
    fall.step(`帖子信息:
ID: ${rawPost.id}
标题: ${rawPost.title}
内容: ${rawPost.content}
作者: ${rawPost.user.nickname}
回复数量: ${rawPost.n_replies}`);
}

async function exportPosts(app: App, db: Database) {
    const comDB = new Community(app, db);
    let fall = new FallTask(app);

    await comDB.sync();

    let count = await comDB.getTotalNumber(), path = app.options["file"] || resolve(app.config.tempDir, `exports_posts-${Date.now()}.csv`);
    if (count <= 0) {
        app.UI.color.yellow("没有帖子可以导出");
        return;
    }
    if (!await app.UI.confirm(
        `你确定要导出所有的帖子吗？该操作将会影响 ${app.UI.color.red(count.toString())} 条帖子！`
    )) return;

    fall.start(`导出 ${app.UI.color.yellow(count.toString())} 条帖子`);
    await fall.waitForLoading(async (resolve, reject) => {
        let posts = await comDB.getAllPosts();
        if (Rejected.isRejected(posts)) {
            reject(posts.toString());
            return;
        }
        let headers = Object.keys(posts[0].get()).map(v=>({
            title: v,
            id: v
        })), data = posts.map(v=> {
            let r = v.get();
            return Object.fromEntries(Object.entries(r).map(([k, v]: [any, any]) => [k, 
                typeof v === "object" && v !== null ? JSON.stringify(v) : v
            ]));
        });
        await writeJSONToCSV(data, headers, path);
        resolve("");
        return;
    }, "正在导出…");

    fall.end(`导出完成: ${app.UI.color.gray(path)}`);
    return;
}

async function scrapePosts(app: App, db: Database) {
    const client = new CodeMaoClient({ app });
    const comDB = new Community(app, db);
    const scraper = new CommunityScraper(app, client);
    let fall = new FallTask(app);

    await comDB.sync();

    const target = await (await app.UI.selectByObject("请选择爬取目标", {
        "特定ID帖子": async () => [await fall.input("请输入帖子ID")],
        "帖子ID范围": async () => {
            const start = parseInt(await fall.input("请输入起始ID", {
                validate: (v) => !isNaN(parseInt(v)),
            }));
            const end = parseInt(await fall.input("请输入结束ID", {
                validate: (v) => !isNaN(parseInt(v)),
            }));
            if (end < start) {
                throw new Error("结束ID不能小于起始ID");
            }
            return { start, end };
        },
        // "获取前300条帖子": async () => {
        //     let posts = await client.api.getHotsPosts();
        //     if (Rejected.isRejected(posts)) {
        //         throw new Error(posts.toString());
        //     }
        //     return posts;
        // }
    }))() as (string | number)[] | {
        start: number;
        end: number;
    };

    app.Logger.debug(`开始爬取帖子: ${JSON.stringify(target)}`);
    fall.start(`开始爬取帖子: ${
        Array.isArray(target) ?(
            target.length > 1 ? `${target.length}条帖子` : `帖子${target[0]}`
        ) : `${target.start} ~ ${target.end}`
    }`);

    let i = Array.isArray(target) ? 0 : target.start;
    let nextPost = Array.isArray(target) ?
        (function* () {
            while (i < target.length) {
                yield target[i++];
            }
        }) :
        (function* () {
            while (i <= target.end) {
                yield i++;
            }
        });

    let pool = new TaskPool(5, 1000);

    app.Logger.debug(`开启池子`);
    let progr = await fall.waitForProgress<(CommunityAPI.Post | Rejected)[]>(async (resolve, reject, progress) => {

        app.Logger.debug(`开始爬取帖子`);
        return await new Promise<(CommunityAPI.Post | Rejected)[]>((r, j) => {
            let posts: (CommunityAPI.Post | Rejected)[] = [];
            for (let post of nextPost()) {
                pool.addTask(async () => {
                    if (await comDB.isIdExists(post.toString())) {
                        progress.incrementTask();
                        progress.setText(`${app.UI.color.gray("帖子" + post + "已存在")}`);
                        return;
                    }

                    let data = await scraper.getPost(post.toString());
                    progress.incrementTask();
                    if (Rejected.isRejected(data)) {
                        // progress.log(`${app.UI.color.red("获取" + post + "失败: " + data.toString())}`);
                        progress.setText(`${app.UI.color.gray("获取" + post + "失败: " + data.toString())}`);
                        posts.push(data);
                        await comDB.insertEmpty(post.toString());
                    } else {
                        posts.push(data);
                        await comDB.insert(data);
                    }
                    progress.setText(`${app.UI.color.gray("帖子" + post + "已获取")}`);

                });
            }
            pool.start()
                .then(() => {
                    resolve("");
                    r(posts);
                })
                .catch(() => {
                    reject("");
                    j(posts);
                });
        });
    }, "正在初始化…", Array.isArray(target) ? target.length : target.end - target.start + 1);
    let success = progr.filter(v => !Rejected.isRejected(v)) as CommunityAPI.Post[];
    let failed = progr.filter(Rejected.isRejected) as Rejected[];
    fall.end(app.UI.color.cyan(`成功获取${success.length}条帖子; 失败${failed.length}条帖子`));

}

async function initDB(app: App, file: string) {
    let db = new Database({
        file,
        app,
    });
    let auth = await db.authenticate();
    if (Rejected.isRejected(auth)) return auth;
    return db;
}
