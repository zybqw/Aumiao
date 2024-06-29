import { ModelStatic, DataTypes } from '@sequelize/core';
import { App } from '../../../app.js';
import { Database } from './db.js';
import { CommunityAPI } from '../../../types/api.js';
import { FindOptions, Model, Op, QueryTypes, SyncOptions } from 'sequelize';
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
            is_cached: DataTypes.INTEGER,
            user: {
                type: DataTypes.JSON,
                get() {
                    return this.getDataValue('user') as CommunityAPI.User;
                },
                set(value: CommunityAPI.User) {
                    this.setDataValue('user', value);
                }
            },
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
    sync(options?: SyncOptions) {
        return this.model.sync(options as any);
    }
    insert(data: Partial<CommunityAPI.Post> & {
        is_cached: boolean | number;
    }) {
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
    getFlags(data: Partial<CommunityAPI.Post>): number[] {
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
    async getPostById(id: string, options?: FindOptions): Promise<CommunityAPI.PostDetails | Rejected> {
        try {
            return (await this.model.findOne({
                where: { id },
                ...(options || {}) as any
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

    async matchByTitle(title: string, options?: FindOptions) {
        return this.model.findAll({
            where: {
                title: {
                    [Op.like]: `%${this.replaceQuery(title)}%`
                }
            },
            ...(options || {}) as any
        });
    }
    async matchByContent(content: string, options?: FindOptions) {
        return this.model.findAll({
            where: {
                content: {
                    [Op.like]: `%${this.replaceQuery(content)}%`
                }
            },
            ...(options || {}) as any
        });
    }
    async deletePostById(id: string) {
        return this.model.destroy({
            where: { id }
        });
    }
    replaceQuery(query: string) {
        return query.replace(
            /[\[\]{}()*+?.,\\^$|#\s]/g,
            '\\$&'
        );
    }
    async select(query: string): Promise<unknown[]> {
        const [results] = await this.database.sequelize.query(query, {
            type: QueryTypes.SELECT,
        });
        return [results];
    }
    async updateById(id: string, data: Partial<CommunityAPI.Post>) {
        return this.model.update(data, {
            where: { id }
        });
    }
}
