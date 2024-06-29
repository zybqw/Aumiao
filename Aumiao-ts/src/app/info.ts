import { App } from "../app.js";
import { CodeMaoClient } from "../client/CodeMaoClient.js";
import { Opt } from "../commands.js";
import { UserAPI } from "../types/api.js";
import { FallTask, Rejected } from "../utils.js";

export default async function main(app: App) {
    let fall = new FallTask(app);
    fall.start(`从 ${app.UI.color.blue("shequ.codemao.cn")} 获取用户信息`);

    const state = {
        client: new CodeMaoClient({ app }),
        id: app.options[Opt.id] || await fall.input("请输入用户ID:"),
    };

    fall.step(`${app.UI.color.gray("正在获取用户: " + state.id)}`);
    let user = await fall.waitForLoading<UserAPI.Honor | null>(async (resolve, reject, setText) => {
        let res = await state.client.api.getHonor(state.id);
        if (Rejected.isRejected(res)) {
            reject("获取用户信息失败: " + res.toString() + "\nhttp信息码: " + res.code);
            return null;
        }
        resolve(app.UI.color.green("完成"));
        return res;
    }, "请求信息中…");
    fall.step("");

    if (!user) {
        fall.end(app.UI.color.red("获取用户信息失败"));
        return;
    }
    showUserInfo(app, fall, user);
    fall.end(app.UI.color.gray("获取用户信息成功"));
}

export function showUserInfo(app: App, fall: FallTask, user: UserAPI.Honor) {
    fall.step(`用户信息:
ID: ${user.user_id}
昵称: ${user.nickname}
描述: ${user.user_description}
粉丝数量: ${user.fans_total}
总浏览数: ${user.view_times}
总点赞数: ${user.liked_total}`);
}
