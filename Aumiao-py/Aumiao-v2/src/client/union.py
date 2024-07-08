import src.app.acquire as acquire
import src.app.data as data
import src.client.user as user
import src.client.work as work


class WorkUnion:

    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.user = user.User()
        self.work = work.Work()
        self.data = data.CodeMaoData()

    # 清除作品广告的函数
    def clear_ad(self, keys) -> bool:
        works_list = self.user.get_user_works(self.data.ACCOUNT_DATA["id"])
        for item0 in works_list:
            comments = self.work.get_comments_detail(
                work_id=item0["id"], method="comments"
            )
            work_id = item0["id"]
            for item1 in comments:
                comment_id = item1["id"]
                content = item1["content"].lower()  # 转换小写
                if (
                    any(item2 in content for item2 in keys)
                    and not item1["is_top"]  # 取消置顶评论监测
                ):
                    print(
                        "在作品 {} 中发现广告: {} ".format(item0["work_name"], content)
                    )
                    response = self.acquire.send_request(
                        url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}",
                        method="delete",
                    )
                    print("*" * 50)
                    if response.status_code != 204:
                        return False
        return True


class CommunityUnion:

    def __init__(self) -> None:
        self.work = work.Work()
        self.user = user.User()

    # 给某人作品全点赞
    def like_all_work(self, user_id: str):
        works_list = self.user.get_user_works(user_id)
        for item in works_list:
            if not self.work.like_work(work_id=item["id"]):
                return False
        return True
