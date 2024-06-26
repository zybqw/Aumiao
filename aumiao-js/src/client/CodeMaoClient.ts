import { App } from "../app.js"
import { LoginStored, LoginType } from "../app/login.js";
import { Rejected, readObject } from "../utils.js";
import { AuthProvider } from "./auth.js";
import { Cred, LoginInfo } from "./auth/cred.js";
import { ua } from "./ua.js";

type CodeMaoClientConfig = {
    app: App;
}


type UserDetails = {
    id: string;
    nickname: string;
    avatar_url: string;
    email: string;
    gold: number;
    qq: string;
    real_name: string;
    sex: 'FEMALE' | 'MALE';
    username: string;
    voice_forbidden: boolean;
    birthday: number;
    description: string;
    phone_number: string;
    create_time: number;
    oauths: Array<object>;
    has_password: boolean;
    user_type: number;
    show_guide_flag: number;
    has_signed: boolean;
    has_seen_primary_course: number;
    author_level: number;
};

export class CodeMaoClient {
    static BASE_URL = "https://api.codemao.cn";
    static ENDPOINTS = {
        login: "/tiger/v3/web/accounts/login"
    };
    app: App;
    ua: string;

    authProvider: AuthProvider | null = null;
    token: string = "";
    loginInfo: LoginInfo | null = null;
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
            this.token = this.loginInfo?.auth.token || "";
        }

        if (!this.token || !this.loginInfo) {
            this.app.Logger.error("登录失败！");
            this.app.exit(this.app.App.EXIT_CODES.ERROR);
            return;
        }

        return this;
    }
    getAuthProvider(type: LoginType) {
        return Reflect.construct(({
            [LoginType.Credentials]: Cred,
            [LoginType.Cookie]: Cred
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
            return new Rejected(`Request failed with status ${res.status}: ${res.statusText}`);
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

    public async syncDetails() {
        let details = await this.request<UserDetails>("/web/users/details", {
            method: "GET"
        });
        if (Rejected.isRejected(details)) {
            this.app.Logger.error("Failed to get user details");
            return null;
        }
        this.userDetails = details as UserDetails;
        return this.userDetails;
    }
}

