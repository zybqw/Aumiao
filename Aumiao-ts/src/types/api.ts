
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
