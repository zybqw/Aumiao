import { App } from "../app.js";
import Commands from "../commands.js";

export async function route(name: string, app: App) {
    app.Logger.debug(`Routing to ${name}`);
    const routes = {
        "index": () => import("./index.js"),
        ...Object.fromEntries(Commands.map(({ name, file }) => [name, () => import(`./${file}`)]))
    };
    return name in routes ? (await (routes[name as keyof typeof routes]()))?.default(app) : null;
}
