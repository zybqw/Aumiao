import { App } from "../app.js"
import { LoginStored, LoginType } from "../app/login.js";
import { MessageCount, UserDetails } from "../types/api.js";
import { Rejected, readObject } from "../utils.js";
import { AuthProvider } from "./auth.js";
import { Cookie } from "./auth/cookie.js";
import { Cred, EnvCred } from "./auth/cred.js";
import { ua } from "./ua.js";

type CodeMaoClientConfig = {
    app: App;
}


export type LoggedData = {
    id: string;
    nickname: string;
    token: string;
}

export class CodeMaoClient {
    static BASE_URL = "https://api.codemao.cn";
    static ENDPOINTS = {
        login: "/tiger/v3/web/accounts/login",
        message_record: "/web/message-record/count",
        user_details: "/web/users/details"
    };
    app: App;
    ua: string;

    authProvider: AuthProvider | null = null;
    token: string = "";
    loginInfo: LoggedData | null = null;
    userDetails: UserDetails | null = null;
    constructor(protected config: CodeMaoClientConfig) {
        this.app = config.app;
        this.ua = ua();

        this.app.Logger.verbose("CodeMaoClient initialized");
    }
    async tryLogin(loginStored?: LoginStored, type: LoginType = LoginType.Credentials) {
        this.app.Logger.verbose("trying to login: " + type);
        if (loginStored && readObject((loginStored || {}).data, "token")) {
            this.token = readObject(loginStored.data, "token") as string;
        } else {
            this.authProvider = this.getAuthProvider(type);
            this.loginInfo = await this.authProvider.login();
            this.token = this.loginInfo?.token || "";
        }

        if (!this.token || !this.loginInfo) {
            this.app.Logger.error("登录失败！");
            this.app.exit(this.app.App.EXIT_CODES.ERROR);
            return;
        }

        return this;
    }
    getAuthProvider(type: LoginType): AuthProvider {
        return Reflect.construct(({
            [LoginType.Credentials]: Cred,
            [LoginType.Cookie]: Cookie,
            [LoginType.EnvCred]: EnvCred
        })[type], [this.app, this])
    }
    async request<T>(endpoint: string, options: RequestInit): Promise<T | Rejected> {
        this.app.Logger.verbose(`requesting ${endpoint} with options: ${JSON.stringify(options)}`);
        const res = await fetch(CodeMaoClient.BASE_URL + endpoint, {
            ...options,
            headers: {
                "User-Agent": this.ua,
                "Content-Type": "application/json",
                ...(options.headers || {}),
                ...(this.token ? {
                    "cookie": "authorization=" + this.token
                }: {})
            }
        });
        if (!res.ok) {
            return new Rejected(`Request failed with status ${res.status}: ${res.statusText}`, res.status);
        }
        return await res.json() as T;
    }

    public getStorableData(): LoginStored {
        return {
            data: {
                token: this.token
            }
        };
    }

    private async requestEndpoint<T>(endpoint: string, options: RequestInit, silent = false): Promise<T | null> {
        let res = await this.request<T>(endpoint, options);
        if (Rejected.isRejected(res)) {
            if (!silent) this.app.Logger.error("Failed to request endpoint: " + endpoint + "\n" + res.toString());
            return null;
        }
        return res;
    }

    public async syncDetails(silent = false) {
        return await this.requestEndpoint<UserDetails>(CodeMaoClient.ENDPOINTS.user_details, {
            method: "GET"
        }, silent);
    }

    public async getMessageRecordCound() {
        return await this.requestEndpoint<MessageCount[]>(CodeMaoClient.ENDPOINTS.message_record, {
            method: "GET"
        });
    }
}

