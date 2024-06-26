import type { UI } from "./types/ui.js";
import { Logger, isFileExist } from "./utils.js";

import * as commander from "commander";
import path from "path";
import { EventEmitter } from "events";

import { CommandDefinition, ProgramDefinision } from "./types/command.js";
import { route } from "./app/router.js";

import { config } from "dotenv";

const { program, Option } = commander;

export type AppConfig = {
    debug: boolean;
    verbose: boolean;
    envFile: string;
    tempDir: string;
    allowStore: boolean;
}
export type EnvConfig = {
    PASSWORD: string;
    USERNAME: string;
}

export class App {
    static DefaultConfig: AppConfig = {
        debug: false,
        verbose: false,
        envFile: path.resolve(import.meta.dirname, "../.env"), // equals to path.resolve(__dirname, "../.env")
        tempDir: path.resolve(import.meta.dirname, "../temp"),
        allowStore: true,
    };
    static DefaultEnvConfig: EnvConfig = {
        PASSWORD: "",
        USERNAME: "",
    };
    static StaticConfig = {
        MAX_TRY: 128,
        ART_TEXT: `
 ________  ___  ___  _____ ______   ___  ________  ________                     ___  ________      
|\\   __  \\|\\  \\|\\  \\|\\   _ \\  _   \\|\\  \\|\\   __  \\|\\   __  \\                   |\\  \\|\\   ____\\     
\\ \\  \\|\\  \\ \\  \\\\\\  \\ \\  \\\\\\__\\ \\  \\ \\  \\ \\  \\|\\  \\ \\  \\|\\  \\  ____________    \\ \\  \\ \\  \\___|_    
 \\ \\   __  \\ \\  \\\\\\  \\ \\  \\\\|__| \\  \\ \\  \\ \\   __  \\ \\  \\\\\\  \\|\\____________\\__ \\ \\  \\ \\_____  \\   
  \\ \\  \\ \\  \\ \\  \\\\\\  \\ \\  \\    \\ \\  \\ \\  \\ \\  \\ \\  \\ \\  \\\\\\  \\|____________|\\  \\\\_\\  \\|____|\\  \\  
   \\ \\__\\ \\__\\ \\_______\\ \\__\\    \\ \\__\\ \\__\\ \\__\\ \\__\\ \\_______\\            \\ \\________\\____\\_\\  \\ 
    \\|__|\\|__|\\|_______|\\|__|     \\|__|\\|__|\\|__|\\|__|\\|_______|             \\|________|\\_________\\
                                                                                       \\|_________|`,
    };
    static EXIT_CODES = {
        SUCCESS: 0,
        ERROR: 1,
    };
    static EVENTS = {
        START: "start",
        STOP: "stop",
    };


    UI: typeof UI;
    config: AppConfig;
    Logger: Logger;
    events: EventEmitter = new EventEmitter();
    program: commander.Command;
    App: typeof App = App;
    commands: { [name: string]: commander.Command };
    envConfig: EnvConfig = App.DefaultEnvConfig;

    get options() {
        return this.program.opts();
    }

    constructor({
        UIUtils,
        config,
    }: {
        UIUtils: typeof UI,
        config: Partial<AppConfig>,
    }) {
        this.UI = UIUtils;
        this.config = { ...this.App.DefaultConfig, ...config };

        this.program = program;
        this.Logger = new Logger(this);
        this.commands = {};
    }

    public async start() {
        this.events.emit(App.EVENTS.START);
        this.program.parse(process.argv);
        this.Logger.verbose("App started");
        await this.loadEnv();
    }

    public registerProgram({ name, description, version }: ProgramDefinision) {
        this.program.name(name)
            .description(description)
            .version(version)
            .action(async () => {
                await route("index", this);
            }).option("-v, --verbose", "Enable verbose logging", () => {
                this.config.verbose = true;
            }).option("-d, --debug", "Enable debug logging", () => {
                this.config.debug = true;
            });
        return this;
    }
    public registerCommand(command: CommandDefinition, parent = this.program, root: Record<string, any> = {}) {
        const cmd = new commander.Command(command.name)
            .description(command.description)
            .action(async () => {
                await this.runCommand(cmd, command);
            });
        command.options?.forEach(option => {
            cmd.option(option.flags, option.description, option.defaultValue);
        });
        parent.addCommand(cmd);
        root[command.name] = { ...command, command: cmd, children: {} };
        if (command.children) this.registerCommands(command.children, cmd, root[command.name].children);
        return this;
    }
    public registerCommands(commands: CommandDefinition[], parent = this.program, root: Record<string, any> = {}) {
        commands.forEach(command => {
            this.registerCommand(command, parent, root);
        });
        return this;
    }

    protected async runCommand(command: commander.Command, config: CommandDefinition) {
        try {
            await route(config.name, this);
        } catch (err) {
            this.Logger.error("Crashed while executing the command: " + config.name || command.name());
            this.Logger.error(err as any);
            this.exit(this.App.EXIT_CODES.ERROR);
        }
    }

    async loadEnv() {
        let file = this.options["env"] || this.config.envFile;
        if ((!this.options["env"] && !this.config.envFile) || !(await isFileExist(
            file
        ))) {
            this.Logger.warn("无可用的env文件或无法访问该文件" + (file? `: ${file}` : ""));
            return;
        }
        let parsed = config({
            path: this.config.envFile,
            override: true,
        });
        if (parsed.error) {
            this.Logger.error("尝试读取.env文件时出错: " + parsed.error.message);
            return;
        }
        this.envConfig = { ...this.envConfig, ...(parsed.parsed || {}) };
    }

    on(event: string, listener: (...args: any[]) => void) {
        this.events.on(event, listener);
    }
    emit(event: string, ...args: any[]) {
        this.events.emit(event, ...args);
    }

    exit(code: number) {
        process.exit(code);
    }
}

