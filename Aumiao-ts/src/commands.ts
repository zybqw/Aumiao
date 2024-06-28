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
    },
    "sensei": {
        flags: "-n, --no-sensei",
        description: "禁止让面板叫你Sensei",
    },
    "force": {
        flags: "-F, --force",
        description: "强制执行",
        defaultValue: false
    }
}
const Opt: Record<keyof typeof Options, any> = Object.fromEntries(Object.entries(Options).map(([key]) => [key, key])) as Record<keyof typeof Options, any>;

const Commands: CommandDefinition[] = [
    {
        name: "login",
        description: "登录社区（单账户）",
        options: [Options.allowStore, Options.file, Options.env],
    },
    {
        name: "update",
        description: "更新整个Aumiao项目",
        options: [Options.force],
    }
]

const GlobalOptions: {
    flags: string;
    description: string;
    defaultValue?: any;
}[] = [Options.env, Options.sensei]

export default Commands;
export {
    GlobalOptions,
    Opt
}
