
export namespace UserAPI {
    /**
     * @deprecated
     */
    export type OtherUser = {
        userInfo: {
            user: {
                id: number;
                nickname: string;
                sex: '0' | '1'; // '0' 代表女性，'1' 代表男性
                description: string;
                doing: string;
                preview_work_id: number;
                level: number;
                avatar: string;
            };
            work: JSON; // 封面作品的详细信息，具体结构未知
            collectionTimes: number; // 作品被收藏次数
            forkedTimes: number; // 作品被再创作次数
            isFollowing: JSON; // 未知的 JSON 结构
            praiseTimes: number; // 作品被点赞次数
            viewTimes: number; // 作品被浏览次数
        };
    };
    export type Honor = {
        user_id: number;
        nickname: string;
        avatar_url: string;
        user_cover: string;
        user_description: string;
        doing: string;
        attention_status: boolean;
        block_total: number;
        re_created_total: number;
        attention_total: number;
        fans_total: number;
        collected_total: number;
        collect_times: number;
        liked_total: number;
        view_times: number;
        author_level: number;
        consume_level: number;
        is_official_certification: number;
        subject_id: number;
        work_shop_name: string;
        work_shop_level: number;
        like_score: number;
        collect_score: number;
        fork_score: number;
    }
}

export namespace CommunityAPI {
    export type User = {
        id: string;
        nickname: string;
        avatar_url: string;
        subject_id: number;
        work_shop_name: string;
        work_shop_level: number;
        wuhan_medal: boolean; // unknown
        has_signed: boolean;
    };
    export type Post = {
        id: string; // 帖子 ID
        user: User;
        title: string; // 帖子标题
        content: string; // 帖子内容
        board_id: string; // 帖子所在板块 ID
        board_name: string; // 帖子所在板块名称
        updated_at: number; // 更新时间戳
        created_at: number; // 发布时间戳
        n_views: number; // 浏览次数
        n_replies: number; // 回帖数量
        n_comments: number; // （每个回帖下的）评论数量
        is_authorized: boolean; // 是否为官方贴
        is_featured: boolean; // 是否为精选贴
        is_hotted: boolean; // 是否为热门贴
        is_pinned: boolean; // 是否为置顶帖
        tutorial_flag: 0 | 1; // 是否为教程帖
        ask_help_flag: 0 | 1; // 是否为求助帖
    };
    export type Reply = {
        id: string;
        user: User;
        is_top: boolean;
        n_likes: number;
        is_liked: boolean;
        content: string;
        n_comments: number;
        created_at: number;
        updated_at: number;
        earliest_comments: {
            id: string;
            user: User;
            n_likes: number;
            is_liked: boolean;
            content: string;
            created_at: number;
        }[];
    };
    export type Replies = {
        items: Reply[];
        offset: number;
        limit: number;
        total: number;
        counted: boolean; // unknown
    };
    export type Hots = {
        items: number[];
    }
}

export type UserDetails = {
    id: string;
    nickname: string;
    avatar_url: string;
    email: string;
    gold: number;
    qq: string;
    real_name: string;
    sex: 'FEMALE' | 'MALE';
    username: string;
    voice_forbidden: boolean;
    birthday: number;
    description: string;
    phone_number: string;
    create_time: number;
    oauths: Array<object>;
    has_password: boolean;
    user_type: number;
    show_guide_flag: number;
    has_signed: boolean;
    has_seen_primary_course: number;
    author_level: number;
};

export type MessageCount = {
    query_type: "COMMENT_REPLY" | "LIKE_FORK" | "SYSTEM",
    count: number;
}
