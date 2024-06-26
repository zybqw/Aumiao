import { App } from "../app.js";

export async function route(name: string, app: App) {
    app.Logger.debug(`Routing to ${name}`);
    const routes = {
        "index": () => import("./index.js"),
        "login": () => import("./login.js"),
    };
    return name in routes ? (await (routes[name as keyof typeof routes]()))?.default(app) : null;
}
