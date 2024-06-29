import { App } from "../../app.js";
import { CommunityAPI } from "../../types/api.js";
import { Rejected } from "../../utils.js";
import { CodeMaoClient } from "../CodeMaoClient.js";


export class CommunityScraper {
    constructor(protected app: App, protected client: CodeMaoClient) { }
    public async getPost(postId: string): Promise<CommunityAPI.Post & { replies: CommunityAPI.Reply[] } | Rejected> {
        let [postDetails, postReplies] = await Promise.all([
            this.client.api.getPostDetails(postId),
            this.getReplies(postId)
        ]);
        let rejected = [postDetails, postReplies].find(Rejected.isRejected);
        return rejected || { ...postDetails, replies: postReplies as CommunityAPI.Reply[] };
    }
    public async getReplies(postId: string): Promise<CommunityAPI.Reply[] | Rejected> {
        let replies: CommunityAPI.Reply[] = [];
        let page = 1, limit = 30;
        let f = await this.client.api.getPostReplies(postId, page, limit);

        if (Rejected.isRejected(f)) {
            return f;
        }
        replies.push(...f.items);

        while (replies.length < f.total) {
            let reply = await this.client.api.getPostReplies(postId, ++page, limit);
            if (Rejected.isRejected(reply)) {
                return reply;
            }
            replies.push(...reply.items);
        }
        return replies;
    }
}
