import { App } from "../../app.js";
import { FallTask } from "../../utils.js";
import { CodeMaoClient, LoggedData } from "../CodeMaoClient.js";
import { UserDetails } from "../../types/api.js";
import { AuthProvider } from "../auth.js";

export class Cookie implements AuthProvider {
    constructor(protected app: App, protected client: CodeMaoClient) {}

    token: string = "";
    async login(): Promise<LoggedData | null> {
        const state: {
            authorization: string;
        } = {
            authorization: ""
        };
        const fall = new FallTask(this.app);
        fall.start(this.app.UI.color.blue("登录codemao.cn"));

        while (!state.authorization) {
            state.authorization = await fall.input("请输入你的cookie:");
            if (!state.authorization) {
                fall.error("Cookie不能为空！\n如果你需要寻找你的cookie，请查看 https://github.com/zybqw/Aumiao/blob/main/Aumiao-ts/docs/how-to-get-cookie.md");
            }
        }

        let res = await fall.waitForLoading<UserDetails | null>(async (resolve, reject) => {
            this.client.token = state.authorization;
            let r = await this.client.syncDetails(true);
            if (r) resolve("");
            else reject("登录失败！");
            return r;
        }, "正在登录…");

        if (res) {
            fall.end(this.app.UI.color.green("登录成功！"));
            return {
                ...res,
                token: state.authorization
            };
        } else {
            fall.end(this.app.UI.color.red("登录失败！"));
            return null;
        }
    }
    async isLogin(): Promise<boolean> {
        return !!(await this.client.syncDetails(true));
    }
}
