import { Sequelize, Model } from '@sequelize/core';
import { OPEN_CREATE, OPEN_READWRITE, SqliteDialect } from '@sequelize/sqlite3';
import { App } from '../../../app.js';
import { Rejected } from '../../../utils.js';

export type DatabaseConfig = {
    file: string;
    app: App;
}

export class Database {
    static defaultConfig: DatabaseConfig = {
        file: "community.sqlite",
        app: null as unknown as App
    };

    sequelize: Sequelize<SqliteDialect>;
    config: DatabaseConfig;
    app: App;
    constructor(config: Partial<DatabaseConfig> = {}) {
        this.config = this.mergeConfig(config);
        this.app = this.config.app;
        this.sequelize = new Sequelize({
            dialect: SqliteDialect,
            storage: this.config.file,
            mode: OPEN_CREATE | OPEN_READWRITE,
            logging: this.app.Logger.verbose.bind(this.app.Logger)
        });
    }

    mergeConfig(config: Partial<DatabaseConfig>): DatabaseConfig {
        return { ...Database.defaultConfig, ...config };
    }
    async authenticate(): Promise<boolean | Rejected> {
        try {
            await this.sequelize.authenticate();
            this.app.Logger.verbose('Connection has been established successfully.');
            return true;
        } catch (error: any) {
            return new Rejected(error);
        }
    }
    close() {
        this.sequelize.close();
    }
}
