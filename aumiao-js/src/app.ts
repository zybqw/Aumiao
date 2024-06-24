import { UI } from "./types/ui";
import { Logger } from "./utils";

export type AppConfig = {
    debug: boolean;
    verbose: boolean;
}

export class App {
    UI: typeof UI;
    config: AppConfig;
    Logger: Logger;
    constructor({
        UIUtils,
        config,
    }: {
        UIUtils: typeof UI,
        config: AppConfig,
    }) {
        this.UI = UIUtils;
        this.config = config;

        this.Logger = new Logger(this);
    }
}

