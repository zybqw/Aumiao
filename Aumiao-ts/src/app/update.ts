import { App } from "../app.js";
import { Opt } from "../commands.js";
import { FallTask, execBash } from "../utils.js";
import { rm } from 'fs/promises';

async function deleteDirectories(directories: string[]) {
    for (const dir of directories) {
        await rm(dir, { recursive: true, force: true });
    }
}

export default async function main(app: App) {
    app.Logger.tagless(app.App.StaticConfig.ART_TEXT);

    let fall = new FallTask(app);
    fall.start("当前版本：" + app.version);
    let task = await fall.waitForLoading(async (resolve, reject, setText) => {
        try {
            if (app.options[Opt.force]) {
                setText("正在清理缓存…");
                await deleteDirectories(['./node_modules/', './dist/', '../.git/']);
            }
            await execBash("git checkout main && git checkout . && git reset --hard && git pull origin main");
            setText("坐和放宽，我们正在重新安装…");
            await execBash("node ./scripts/install.js");
            resolve("完成");
            return true;
        } catch (err) {
            reject("遇到了些问题\n" + err + "\n请稍后重新尝试，如果问题依旧存在，请尝试node aumiao update --force或手动更新");
            return null;
        }
    }, "正在从仓库拉取新版本…");
    if (!task) {
        fall.end(app.UI.color.red("更新失败！"));
    } else {
        fall.end(app.UI.color.green("大功告成"));
    }
    return;
}
