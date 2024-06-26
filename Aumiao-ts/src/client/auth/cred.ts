import { App } from "../../app.js";
import { FallTask, Rejected } from "../../utils.js";
import { CodeMaoClient } from "../CodeMaoClient.js";
import { AuthProvider } from "../auth.js";


export type LoginInfo = {
    user_info: {
        id: number;
        nickname: string;
        avatar_url: string;
        fullname: string;
        sex: 0 | 1;
        birthday: number;
        qq: string;
        description: string;
    };
    auth: {
        token: string;
        email: string;
        phone_number: string;
        has_password: boolean;
        is_weak_password: number;
    }
}

export class Cred implements AuthProvider {
    static LOGIN_PID = "65edCTyg";
    constructor(protected app: App, protected client: CodeMaoClient) {}

    token: string = "";
    async login(): Promise<LoginInfo | null> {
        const state: {
            username: string;
            password: string;
        } = {
            username: "",
            password: ""
        };

        const fall = new FallTask(this.app);
        fall.start(this.app.UI.color.blue("登录codemao.cn"));
        if (this.app.envConfig["USERNAME"] && this.app.envConfig["PASSWORD"]) {
            state.username = this.app.envConfig["USERNAME"];
            state.password = this.app.envConfig["PASSWORD"];
        } else {
            state.username = await fall.input("用户名:");
            state.password = await fall.password("密码:");
        }
        fall.step(this.app.UI.color.gray("正在登录…"), 1);
        fall.step(this.app.UI.color.gray("发送请求…"));

        let res = await this._SendLoginRequest(state.username, state.password);
        if (!Rejected.isRejected(res) && (res as LoginInfo).auth.token) {
            fall.end(this.app.UI.color.green("登录成功！"));

            this.token = (res as LoginInfo).auth.token;
            return (res as LoginInfo);
        } else {
            fall.error("登录失败！\n" + (res as Rejected).toString());
            fall.end(this.app.UI.color.red("登录失败！"));
            return null;
        }
    }
    async isLogin(): Promise<boolean> {
        throw new Error("Method not implemented.");
    }
    private async _SendLoginRequest(username: string, password: string): Promise<LoginInfo | Rejected> {
        return this.client.request<LoginInfo>(CodeMaoClient.ENDPOINTS.login, {
            method: "POST",
            body: JSON.stringify({
                pid: Cred.LOGIN_PID,
                identity: username,
                password
            })
        })
    }
}
