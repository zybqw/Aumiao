import { ModelStatic, DataTypes } from '@sequelize/core';
import { App } from '../../../app.js';
import { Database } from './db.js';
import { CommunityAPI } from '../../../types/api.js';
import { Model, Op } from 'sequelize';
import { Rejected } from '../../../utils.js';

type StoredFlags = Pick<
    CommunityAPI.Post,
    'is_authorized'
    | 'is_featured'
    | 'is_hotted'
    | 'is_pinned'
    | 'tutorial_flag'
    | 'ask_help_flag'
>;

export class Community {
    static Flags: {
        [K in keyof StoredFlags]: number
    } = {
            is_authorized: 0,
            is_featured: 1,
            is_hotted: 2,
            is_pinned: 3,
            tutorial_flag: 4,
            ask_help_flag: 5
        }

    model: ModelStatic;
    constructor(protected app: App, protected database: Database) {
        this.model = database.sequelize.define('community', {
            id: {
                type: DataTypes.STRING,
                primaryKey: true,
                unique: true
            },
            title: DataTypes.STRING,
            content: DataTypes.STRING,
            board_id: DataTypes.STRING,
            updated_at: DataTypes.DATE,
            created_at: DataTypes.DATE,
            n_views: DataTypes.INTEGER,
            n_replies: DataTypes.INTEGER,
            n_comments: DataTypes.INTEGER,
            replies: {
                type: DataTypes.JSON,
                get() {
                    return !this.getDataValue('replies') ? [] : this.getDataValue('replies').items as CommunityAPI.Reply[];
                },
                set(value: CommunityAPI.Reply[]) {
                    this.setDataValue('replies', { items: value });
                }
            },
            flags: {
                type: DataTypes.JSON,
                get() {
                    return !this.getDataValue('flags') ? [] : this.getDataValue('flags').items as number[];
                },
                set(value: number[]) {
                    this.setDataValue('flags', { items: value });
                }
            }
        });
    }
    sync() {
        return this.model.sync();
    }
    insert(data: CommunityAPI.Post) {
        const {
            is_authorized,
            is_featured,
            is_hotted,
            is_pinned,
            tutorial_flag,
            ask_help_flag,
            ...rest
        } = data;
        return this.model.create({
            ...rest,
            flags: this.getFlags(data),
        });
    }
    insertEmpty(id: string) {
        return this.model.create({
            id,
        });
    }
    getFlags(data: CommunityAPI.Post): number[] {
        let flags: number[] = [];
        Object.keys(Community.Flags).forEach((key) => {
            if (key in data && !!data[key as keyof typeof Community.Flags]) {
                flags.push(Community.Flags[key as keyof typeof Community.Flags]);
            }
        });
        return flags;
    }
    async isIdExists(id: string) {
        return !!(await this.model.findOne({
            where: { id },
            attributes: ['id']
        }));
    }
    async getPostById(id: string): Promise<CommunityAPI.PostDetails | Rejected> {
        try {
            return (await this.model.findOne({
                where: { id }
            }))?.get({
                plain: true
            });
        } catch (e: any) {
            return new Rejected(e);
        }
    }
    async getTotalNumber() {
        return this.model.count();
    }
    async getAllPosts() {
        return this.model.findAll();
    }

    async matchByTitle(title: string) {
        return this.model.findAll({
            where: {
                title: {
                    [Op.like]: `%${this.replaceQuery(title)}%`
                }
            }
        });
    }
    async matchByContent(content: string) {
        return this.model.findAll({
            where: {
                content: {
                    [Op.like]: `%${this.replaceQuery(content)}%`
                }
            }
        });
    }
    replaceQuery(query: string) {
        return query.replace(
            /[\[\]{}()*+?.,\\^$|#\s]/g,
            '\\$&'
        );
    }
}
