import { App } from "./app.js";

import * as path from "path";
import { pathToFileURL } from 'url';

type LogLevel = "INFO" | "ERROR" | "DEBUG" | "WARN" | "LOG" | "VERBOSE" | "UNKNOWN";
type LogLevelConfig = {
    color: string;// typeof UI.Colors[keyof typeof UI.Colors];
    colorMessage?: (v: string) => Promise<string>;
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
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Gray).then((f: (arg0: string) => any) => f(v)),
                name: "INFO"
            },
            ERROR: {
                color: this.app.UI.Colors.Red,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Red).then((f: (arg0: string) => any) => f(v)),
                name: "ERROR"
            },
            DEBUG: {
                color: this.app.UI.Colors.Navy,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Navy).then((f: (arg0: string) => any) => f(v)),
                name: "DEBUG"
            },
            WARN: {
                color: this.app.UI.Colors.Yellow,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Yellow).then((f: (arg0: string) => any) => f(v)),
                name: "WARN"
            },
            LOG: {
                color: this.app.UI.Colors.White,
                name: "LOG"
            },
            VERBOSE: {
                color: this.app.UI.Colors.Gray,
                colorMessage: (v) => this.app.UI.hex(this.app.UI.Colors.Gray).then((f: (arg0: string) => any) => f(v)),
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

    async generate({ level = this.Levels.UNKNOWN, message } : { level: LogLevel, message: string | Error }) {
        return `${this.app.UI.hex(this.LevelConfig[level].color).then((v: (arg0: string) => any)=>v("[" + level + "]"))} ${await this.LevelConfig[level]?.colorMessage?.(
            message instanceof Error ? message.message : message
        ) || message}`;
    }

    log(message: string): Logger;
    log(message: Error): Logger;
    log(message: string | Error): Logger {
        try {
            if (message instanceof Error) message = message.message + "\n" + message.stack;
        } catch { /* empty */ }
        this.generate({ level: this.Levels.LOG, message }).then(v => console.log(v));
        return this;
    }

    warn(message: string): Logger {
        this.generate({ level: this.Levels.WARN, message }).then(v => console.warn(v));
        return this;
    }

    info(message: string): Logger {
        this.generate({ level: this.Levels.INFO, message }).then(v => console.info(v));
        return this;
    }

    error(message: string | Error): Error {
        if (message instanceof Error) message = message.message + "\n" + message.stack;
        this.generate({ level: this.Levels.ERROR, message }).then(v => console.error(v));
        return new Error(message);
    }

    debug(message: string | Error): Logger {
        try {
            if (typeof message !== "string") message = JSON.stringify(message);
        } catch { /* empty */ }
        if (this.app.config.debug) this.generate({ level: this.Levels.DEBUG, message }).then(v => console.debug(v));
        return this;
    }

    verbose(message: string) {
        if (this.app.config.verbose) this.generate({ level: this.Levels.VERBOSE, message }).then(v => console.log(v));
        return this;
    }

    tagless(message: string) {
        console.log(message);
        return this;
    }
}

export class RPM {
    static subscribers: RPM[] = [];
    static intervalId: null | number | NodeJS.Timeout = null;
    interval: number;
    queue: {
        task: (...args: Array<unknown>) => void;
        args: Array<unknown>;
    }[];
    lastRunTimestamp: number;
    static exit() {
        if (RPM.intervalId !== null)clearInterval(RPM.intervalId);
    }

    static tick() {
        for (const subscriber of RPM.subscribers) {
            subscriber.runNextTask();
        }
    }

    constructor(maxRPM: number) {
        this.interval = 60000 / maxRPM;
        this.queue = [];
        this.lastRunTimestamp = 0;
        RPM.subscribers.push(this);
        if (RPM.intervalId === null) {
            RPM.intervalId = setInterval(RPM.tick, this.interval);
        }
    }

    addTask(task: () => void, ...args: undefined[]) {
        this.queue.push({ task, args });
    }

    runNextTask() {
        if (this.queue.length > 0 && Date.now() - this.lastRunTimestamp >= this.interval) {
            const { task, args } = this.queue.shift()!;
            this.lastRunTimestamp = Date.now();
            task(...args);
        }
    }

    createTask(taskFunction: (...args: Array<unknown>) => any, ...args: any[]) {
        return async () => {
            return new Promise(resolve => {
                this.addTask(() => {
                    const f = taskFunction(...args);
                    if (f.then) f.then(resolve);
                    else resolve(f);
                });
            });
        };
    }

    exit() {
        RPM.exit();
    }
}

export class TaskPool {
    maxConcurrent: any;
    delayBetweenTasks: any;
    taskQueue: (() => Promise<unknown>)[];
    running: boolean;
    allTasksDone: null | Promise<unknown>;
    allTasksDoneResolve!: (value: unknown) => void;
    constructor(maxConcurrent: any, delayBetweenTasks: any) {
        this.maxConcurrent = maxConcurrent;
        this.delayBetweenTasks = delayBetweenTasks;
        this.taskQueue = [];
        this.running = false;
        this.allTasksDone = null;
    }

    addTask(asyncTask: any) {
        this.taskQueue.push(asyncTask);
        return this;
    }

    addTasks(asyncTasks: any) {
        this.taskQueue.push(...asyncTasks);
        return this;
    }

    start() {
        this.running = true;
        this.allTasksDone = new Promise(resolve => this.allTasksDoneResolve = resolve);
        this.runTasks();
        return this.allTasksDone;
    }

    runTasks() {
        const tasksPromises = [];
        for (let i = 0; i < this.maxConcurrent && this.taskQueue.length > 0; i++) {
            tasksPromises.push(this.executeNextTask());
        }
        Promise.allSettled(tasksPromises).then(() => {
            if (this.taskQueue.length > 0) {
                this.runTasks();
            } else {
                this.allTasksDoneResolve(void 0);
            }
        });
    }

    async executeNextTask(): Promise<unknown> {
        if (!this.running) return;
        await new Promise(resolve => setTimeout(resolve, this.delayBetweenTasks));
        if (this.taskQueue.length === 0) return;
        const task = this.taskQueue.shift()!;
        return task().finally(() => {
            if (this.running && this.taskQueue.length > 0) {
                return this.executeNextTask();
            }
        });
    }

    stop() {
        this.running = false;
        return this;
    }
}

export async function moduleLoader(mods: string[]) {
    const modules = mods.map(mod => {
        const modulePath = mod.startsWith(".") ? path.resolve("../", mod) : mod;
        const moduleURL = mod.startsWith(".") ? pathToFileURL(modulePath).href : modulePath;
        return import(moduleURL);
    });
    return Promise.all(modules);
}

export class Rejected extends Error {
    static isRejected(r: any) {
        return r instanceof Rejected;
    }

    constructor(message: string | undefined) {
        super(message);
        this.name = "Rejected";
    }
}

export function randomInt(min: number, max: number) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function sleep(ms: number | undefined) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export function isValidUrl(string: string) {
    const urlRegex = /^(https?:\/\/)?((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|((\d{1,3}\.){3}\d{1,3}))(:\d+)?(\/[-a-z\d%_.~+]*)*(\?[;&a-z\d%_.~+=-]*)?(#[-a-z\d_]*)?$/i;
    return urlRegex.test(string);
}
