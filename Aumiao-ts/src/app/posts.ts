import { App } from "../app.js";
import { CodeMaoClient } from "../client/CodeMaoClient.js";
import { CommunityScraper } from "../client/scrape/community.js";
import { Community } from "../client/store/sqlite/community.js";
import { Database } from "../client/store/sqlite/db.js";
import { CommunityAPI } from "../types/api.js";
import { paginate, tableInput } from "../ui.js";
import { FallTask, Rejected, TaskPool, removeHTMLTags, resolve, writeJSONToCSV } from "../utils.js";

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
        "查找帖子": async () => {
            let exited = false;
            while (!exited) {
                await findPost(app, db);
            }
        },
        "导出帖子": () => exportPosts(app, db),
        [app.UI.color.red("编辑源")]: async () => await editTable(app, db),
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

async function editTable(app: App, db: Database) {
    const comDB = new Community(app, db);
    await comDB.sync({
        alter: true
    });

    if (!await app.UI.confirm(`你确定要编辑数据库吗？${app.UI.color.red("该操作会影响数据库的数据，并且无法撤销！")}`)) return;

    let query = await app.UI.input("请输入SQL查询语句（SQLite，仅限select）");
    let result = await comDB.select(query) as CommunityAPI.Post[];

    app.Logger.debug(`查询结果: ${JSON.stringify(result, null, 2)}`);
    if (!result || !result.length) {
        app.Logger.info("没有找到任何数据");
        return;
    }

    let res = await tableInput(
        "communities",
        "表格 communities 的数据",
        Object.keys(result[0]).map(v => ({
            name: v,
            value: v,
            editable: "text",
        })),
        result.map(v => Object.values(v))
    );

    if (!await app.UI.confirm("你确定要保存更改吗？")) return;
    await Promise.all(res["communities"].result.map(v => comDB.updateById(v.id as string, v)));

    app.Logger.info("保存成功");
}

async function findPost(app: App, db: Database) {
    const comDB = new Community(app, db);

    await comDB.sync({
        alter: true
    });

    async function selectPost(posts: {
        id: string;
        title: string;
    }[], keyword: string) {
        return await app.UI.selectByObject("请选择帖子", Object.fromEntries(posts.map(v =>
            [
                v.title.split(keyword).map(v => app.UI.color.gray(v)).join(app.UI.color.yellow(keyword)),
                v
            ]
        )));
    };
    async function selectHighlightedPost(posts: {
        id: string;
        content: string;
    }[], keyword: string) {
        let options = posts.map(v => {
            const content = removeHTMLTags(v.content).replace(/\n/g, "");
            const maxLength = 20;
            const index = content.indexOf(keyword);
            const start = Math.max(index - maxLength, 0);
            const end = Math.min(index + maxLength, content.length);
            let preview = content.slice(start, end);
            preview = `${app.UI.color.gray(start > 0 ? "…" : "")}${
                preview.split(keyword).map(v => app.UI.color.gray(v)).join(app.UI.color.yellow(keyword))
            }${app.UI.color.gray(end < v.content.length ? "…" : "")}`;
            return [preview, v];
        });
        return await app.UI.selectByObject("请选择帖子", Object.fromEntries(options));
    }
    const target = await (await app.UI.selectByObject("请选择查找方式", {
        "匹配标题": async () => {
            let title = await app.UI.input("标题: ");
            return (await selectPost(await comDB.matchByTitle(title, {
                attributes: ["id", "title"]
            }), title))
        },
        "匹配正文": async () => {
            let content = await app.UI.input("正文: ");
            return await (selectHighlightedPost(await comDB.matchByContent(content, {
                attributes: ["id", "content"]
            }), content))
        },
        "ID查找": async () => await comDB.getPostById(await app.UI.input("ID: "), {
            attributes: ["id", "title"]
        }),
    }))();

    if (Rejected.isRejected(target)) {
        app.Logger.error(`查找失败: ${target.toString()}`);
        return;
    }
    app.Logger.debug(JSON.stringify(target, null, 2));
    if (!target || !target.id) {
        app.Logger.info("没有找到任何帖子");
        return;
    }
    await showPost(app, db, target.id);
}

async function showPost(app: App, db: Database, id: string) {
    const comDB = new Community(app, db);
    let fall = new FallTask(app);

    let start = Date.now();

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
    fall.step(`${rawPost.is_cached ? app.UI.color.yellow("帖子为缓存，信息可能不完整") : app.UI.color.gray(new Date(rawPost.created_at).toLocaleString())}
帖子信息:
ID: ${rawPost.id}
标题: ${rawPost.title}
内容: ${rawPost.content}
作者: ${rawPost.user?.nickname || "%未知%"}
回复数量: ${rawPost.n_replies}`);
    fall.end(`任务完成，耗时: ${Date.now() - start}ms`);

    return (await app.UI.selectByObject("请选择操作", {
        "查看回复": async () => await showReplies(app, db, rawPost.replies),
        "返回": () => { },
        [app.UI.color.red("删除")]: async () => {
            if (!await app.UI.confirm(app.UI.color.red("你确定要删除这个帖子吗？"))) return;
            let result = await comDB.deletePostById(id);
            if (Rejected.isRejected(result)) {
                app.Logger.error(`删除失败: ${result.toString()}`);
            } else {
                app.Logger.info(`删除成功`);
            }
        },
    }))();
}

async function showReplies(app: App, db: Database, replies: CommunityAPI.Reply[]) {
    app.Logger.debug(`开始分页回复: ${JSON.stringify(replies, null, 2)}`);
    let exited = false;
    while (!exited) {
        let reply: CommunityAPI.Reply = await app.UI.selectByObject("请选择回复", Object.fromEntries(replies.map(v => [
            `${app.UI.color.gray(v.user?.nickname || "未知")}: ${removeHTMLTags(v.content).replace(/\n/g, "").slice(0, 20)}`,
            v
        ])));
        (await app.UI.selectByObject(`${app.UI.color.gray(reply.user?.nickname || "未知") + ":"} ${reply.content}`, {
            "返回": () => { },
            "结束": () => exited = true,
        }))();
    }
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
        let headers = Object.keys(posts[0].get()).map(v => ({
            title: v,
            id: v
        })), data = posts.map(v => {
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
    }))() as (string | number)[] | {
        start: number;
        end: number;
    };

    app.Logger.debug(`开始爬取帖子: ${JSON.stringify(target)}`);
    fall.start(`开始爬取帖子: ${Array.isArray(target) ? (
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

    let pool = new TaskPool(5, 1000), waitForCached: string[] = [];

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
                        progress.setText(`${app.UI.color.gray("获取" + post + "失败: " + data.toString())}`);
                        posts.push(data);
                        waitForCached.push(String(post));
                    } else {
                        posts.push(data);
                        await comDB.insert({
                            ...data,
                            is_cached: 0,
                        });
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

    let pool2 = new TaskPool(1, 1000);
    let progr2 = await fall.waitForProgress<(CommunityAPI.CachedPost | Rejected)[]>(async (resolve, reject, progress) => {
        return await new Promise<(CommunityAPI.CachedPost | Rejected)[]>((r, j) => {
            let posts: (CommunityAPI.CachedPost | Rejected)[] = [], done = false, finished = 0;
            while (!done) {
                let postIds = waitForCached.splice(0, 30);
                if (postIds.length === 0) {
                    done = true;
                    continue;
                }
                finished += postIds.length;
                pool2.addTask(async () => {
                    let _data = await client.api.getPostCaches(postIds);
                    progress.incrementTask();
                    if (Rejected.isRejected(_data)) {
                        progr.push(_data);
                        await Promise.all(
                            postIds.map(id => comDB.insertEmpty(id))
                        );
                    } else {
                        const { items: data } = _data;
                        posts.push(...data);
                        await Promise.all(
                            data.map(v => (app.Logger.debug("cache" + v.id + JSON.stringify(v, null ,2)),comDB.insert({
                                content: v.content,
                                id: v.id,
                                title: v.title,
                                user: v.user,
                                n_replies: v.n_replies,
                                created_at: v.created_at,
                                n_comments: v.n_comments,
                                is_featured: v.is_featured,
                                is_hotted: v.is_hotted,
                                is_pinned: v.is_pinned,
                                is_authorized: v.is_authorized,
                                tutorial_flag: v.tutorial_flag,
                                ask_help_flag: v.ask_help_flag,

                                is_cached: 1,
                            })))
                        )
                    }
                });
            }
            pool2.start()
                .then(() => {
                    resolve("");
                    r(posts);
                })
                .catch(() => {
                    reject("");
                    j(posts);
                });
        });
    }, "正在从缓存还原已删除的帖子…", waitForCached.length % 30 === 0 ? waitForCached.length / 30 : Math.floor(waitForCached.length / 30) + 1);

    let cached = progr2.filter(v => !Rejected.isRejected(v)) as CommunityAPI.CachedPost[];
    let success = progr.filter(v => !Rejected.isRejected(v)) as CommunityAPI.Post[];
    let failed = progr.filter(Rejected.isRejected) as Rejected[];
    fall.end(app.UI.color.cyan(`成功获取${success.length}条帖子; 失败${failed.length}条帖子; 从缓存还原${cached.length}条帖子`));
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
