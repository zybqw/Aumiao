import { CommandDefinition } from "./types/command.js"

const Options = {
    "allowStore": {
        flags: "-s, --allow-store",
        description: "允许本地储存登录凭据",
        defaultValue: true
    },
    "file": {
        flags: "-f, --file <file>",
        description: "登录凭据文件（要求绝对路径）",
    },
    "env": {
        flags: "-e, --env <env>",
        description: "环境变量文件（要求绝对路径）",
    }
}

const Commands: CommandDefinition[] = [
    {
        name: "login",
        description: "登录社区（单账户）",
        options: [Options.allowStore, Options.file, Options.env],
    }
]

export default Commands;
