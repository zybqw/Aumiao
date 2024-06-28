import { App } from "../app.js";

async function Menu(app: App) {
    const {

    } = app.UI;
}

export default async function main(app: App) {
    app.Logger.tagless(`\n欢迎使用 ${(app.UI.hex(app.UI.Colors.Blue))("Aumiao-JS")}!`);
    app.Logger.tagless('使用中产生的问题请联系: \n    + 项目负责人：猫鱼a（e-mail: zybqw@qq.com  QQ:3611198191）\n    + 子项目开发者：Nomen （QQ: 2418207411）');
}
