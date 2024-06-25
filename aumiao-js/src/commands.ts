import { CommandDefinition } from "./types/command.js"

const Commands: CommandDefinition[] = [
    {
        name: "login",
        description: "登录社区",
        options: [{
            flags: "-s, --allow-store",
            description: "允许本地储存登录凭据",
            defaultValue: true
        }, {
            flags: "-f, --file <file>",
            description: "登录凭据文件（要求绝对路径）",
            defaultValue: ""
        }]
    }
]

export default Commands;
