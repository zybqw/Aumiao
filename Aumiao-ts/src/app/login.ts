import { App } from "../app.js";
import { CodeMaoClient } from "../client/CodeMaoClient.js";
import { Opt } from "../commands.js";
import { FallTask, createDirIfNotExist, deepMergeObject, isFileExist, readJSON, readObject, resolve, writeJSON } from "../utils.js";

export enum LoginType {
    Credentials = "credentials",
    Cookie = "cookie"
}
export type LoginStored = {
    data: {
        token?: string;
    }
}
const defaultStored: LoginStored = {
    data: {}
};

export default async function main(app: App) {
    app.Logger.tagless(app.App.StaticConfig.ART_TEXT);

    const config = {
        allowStore: app.options["allow-store"] || app.config.allowStore,
        file: app.options["file"] || ""
    };
    const state: { file: string, stored: LoginStored, client: CodeMaoClient } = {
        file: "",
        stored: defaultStored,
        client: new CodeMaoClient({ app })
    };

    // if file is not specified, create a new file in the temp directory
    if (config.allowStore && !config.file) {
        state.file = resolve(app.config.tempDir, "login.json");
        if (await isFileExist(state.file)) {
            app.Logger.debug(`file already exists: ${state.file}`);
            state.stored = await readJSON(state.file, app.Logger.error.bind(app.Logger));
        } else {
            await createDirIfNotExist(app.config.tempDir);
            await writeJSON(state.file, defaultStored);
            app.Logger.debug(`created：${state.file}`);
        }

        // if the file is specified, check if it exists
    } else if (config.allowStore) {
        state.file = config.file;
        if (!await isFileExist(config.file)) {
            app.Logger.error("登录凭据文件不存在！");
        } else {

            // read the file
            state.stored = await readJSON(config.file);
        }
    }

    // normal login
    app.Logger.debug(JSON.stringify(state.stored, null, 2));
    if (
        readObject(state.stored.data, "token")?.length
        && !await app.UI.confirm("你已经储存了凭据并且已经准备好用于登录，重新登录会覆盖当前状态，你要重新登录吗？")
    ) {
        state.client.token = readObject(state.stored?.data, "token") as string;
        let fall = new FallTask(app);
        if (
            !await fall.waitForLoading(async (resolve, reject) => {
                let r = await state.client.syncDetails(true);
                if (r) resolve("");
                else reject("本地凭据已过期，请重新登录");
                return r;
            }, "正在登录…")
        ){
            await writeJSON(state.file, defaultStored);
        } else {
            app.Logger.verbose("login state initialized");

            await MainPanel(app, state.client)();
            return;
        }
    }

    // initial login
    app.Logger.verbose("login state initialized");
    let method = await app.UI.selectByObject("登录方式：", {
        "文本凭据": LoginType.Credentials,
        "Cookie": LoginType.Cookie,
    });
    app.Logger.debug(`selected login method: ${method}`);
    await state.client.tryLogin(undefined, method as LoginType);
    if (config.allowStore) {
        await writeJSON(state.file, deepMergeObject(state.stored, state.client.getStorableData()));
        app.Logger.verbose(`stored login data to ${state.file}`);
    }

    await MainPanel(app, state.client)();
    return;
}

export function MainPanel(app: App, client: CodeMaoClient) {
    return async () => {
        const [
            userDetails,
            messageRecord
        ] = await Promise.all([
            client.syncDetails(true),
            client.getMessageRecordCound()
                .then(v => v?.filter(v => v.query_type === "COMMENT_REPLY")
                    .map(v => v.count)
                    .reduce((a, b) => a + b, 0))
        ]);
    
        const panel = [
            `欢迎回来, ${userDetails?.nickname || ""} ${(!app.options[Opt.sensei]) ? "" : "Sensei!"}`,
            `ID: ${userDetails?.id || ""}`,
            `未读消息: ${app.UI.color.yellow(messageRecord? messageRecord.toString() : "0")}`,
        ];

        FallTask.fall(app, panel);
    }
}
