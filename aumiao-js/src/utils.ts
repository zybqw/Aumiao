import { App } from "./app";
import { UI } from "./types/ui";

type LogLevel = "INFO" | "ERROR" | "DEBUG" | "WARN" | "LOG" | "VERBOSE" | "UNKNOWN";
type LogLevelConfig = {
    color: typeof UI.Colors[keyof typeof UI.Colors];
    colorMessage?: (v: string) => string;
    name: string;
};

export class Logger {
    app: App;
    LevelConfig: Record<LogLevel, LogLevelConfig>;
    constructor(app: App) {
        this.app = app;
        this.LevelConfig = {
            INFO: {
                color: this.app.UI.Colors.Gray,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Gray)(v),
                name: "INFO"
            },
            ERROR: {
                color: this.app.UI.Colors.Red,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Red)(v),
                name: "ERROR"
            },
            DEBUG: {
                color: this.app.UI.Colors.Navy,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Navy)(v),
                name: "DEBUG"
            },
            WARN: {
                color: this.app.UI.Colors.Yellow,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Yellow)(v),
                name: "WARN"
            },
            LOG: {
                color: this.app.UI.Colors.White,
                name: "LOG"
            },
            VERBOSE: {
                color: this.app.UI.Colors.Gray,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Gray)(v),
                name: "VERBOSE"
            },
            UNKNOWN: {
                color: this.app.UI.Colors.White,
                name: "-"
            }
        };
    }

    Levels: Record<LogLevel, LogLevel> = {
        INFO: "INFO",
        ERROR: "ERROR",
        DEBUG: "DEBUG",
        WARN: "WARN",
        LOG: "LOG",
        VERBOSE: "VERBOSE",
        UNKNOWN: "UNKNOWN"
    };

    generate({ level = this.Levels.UNKNOWN, message } : { level: LogLevel, message: string | Error }) {
        return `${this.app.UI.hex(this.LevelConfig[level].color)("[" + level + "]")} ${this.LevelConfig[level]?.colorMessage?.(
            message instanceof Error ? message.message : message
        ) || message}`;
    }

    log(message: string): Logger;
    log(message: Error): Logger;
    log(message: string | Error): Logger {
        try {
            if (message instanceof Error) message = message.message + "\n" + message.stack;
        } catch { /* empty */ }
        console.log(this.generate({ level: this.Levels.LOG, message }));
        return this;
    }

    warn(message: string): Logger {
        console.warn(this.generate({ level: this.Levels.WARN, message }));
        return this;
    }

    info(message: string): Logger {
        console.log(this.generate({ level: this.Levels.INFO, message }));
        return this;
    }

    error(message: string | Error): Error {
        if (message instanceof Error) message = message.message + "\n" + message.stack;
        console.error(this.generate({ level: this.Levels.ERROR, message }));
        return new Error(message);
    }

    debug(message: string | Error): Logger {
        try {
            if (typeof message !== "string") message = JSON.stringify(message);
        } catch { /* empty */ }
        if (this.app.config.debug) console.log(this.generate({ level: this.Levels.DEBUG, message }));
        return this;
    }

    verbose(message: string) {
        if (this.app.config.verbose) console.log(this.generate({ level: this.Levels.VERBOSE, message }));
        return this;
    }

    tagless(message: string) {
        console.log(message);
        return this;
    }
}
