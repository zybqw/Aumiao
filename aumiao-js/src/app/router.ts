import { App } from "../app.js";

export async function route(name: string, app: App) {
    const routes = {
        "index": () => import("./index.js")
    };
    return name in routes ? (await (routes[name as keyof typeof routes]()))?.default(app) : null;
}
