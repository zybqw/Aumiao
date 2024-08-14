from typing import Literal

import src.app.acquire as acquire
import src.app.data as data
import src.app.file as file
import src.app.tool as tool
import src.client.user as user
import src.client.work as work
from src.client import community


class Union:

    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.user_obtain = user.Obtain()
        self.work_obtain = work.Obtain()
        self.data = data.CodeMaoData()
        self.tool_process = tool.CodeMaoProcess()
        self.work_motion = work.Motion()
        self.community_obtain = community.Obtain()
        self.file = file.CodeMaoFile()
        self.user_motion = user.Motion()
        self.tool_routine = tool.CodeMaoRoutine()

    # 清除作品广告的函数
    def clear_ad(self, keys) -> bool:
        works_list = self.user_obtain.get_user_works(self.data.ACCOUNT_DATA["id"])
        for item0 in works_list:

            comments = self.work_obtain.get_work_detail(work_id=item0["id"])  # type: ignore
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

    # 获取评论区特定信息
    def get_comments_detail(
        self,
        work_id: int,
        method: Literal["user_id", "comments"] = "user_id",
    ):
        comments = self.work_obtain.get_work_comments(work_id=work_id)
        if method == "user_id":
            result = [item["user"]["id"] for item in comments]
        elif method == "comments":
            result = self.tool_process.process_reject(
                data=comments,
                reserve=["id", "content", "is_top"],
            )
        else:
            raise ValueError("不支持的请求方法")
        return result

    # 给某人作品全点赞
    def like_all_work(self, user_id: str):
        works_list = self.user_obtain.get_user_works(user_id)
        for item in works_list:
            if not self.work_motion.like_work(work_id=item["id"]):  # type: ignore
                return False
        return True

    # 获取新回复(传入参数就获取前*个回复,若没传入就获取新回复数量, 再获取新回复数量个回复)
    def get_new_replies(self, limit: int = 0) -> list[dict[str, str | int]]:
        _list = []
        reply_num = self.community_obtain.get_message_count(method="web")[0]["count"]
        if reply_num == limit == 0:
            return [{}]
        result_num = reply_num if limit == 0 else limit
        offset = 0
        while True:
            limit = sorted([5, result_num, 200])[1]
            response = self.community_obtain.get_replies(
                type="COMMENT_REPLY", limit=limit, offset=offset
            )
            _list.extend(response["items"][:result_num])
            result_num -= limit
            offset += limit
            if result_num <= 0:
                break
        return _list

    # 新增粉丝提醒
    def message_report(self, user_id: str):
        response = self.user_obtain.get_user_honor(user_id=user_id)
        user_data = {
            "user_id": response["user_id"],
            "nickname": response["nickname"],
            "level": response["author_level"],
            "fans": response["fans_total"],
            "collected": response["collected_total"],
            "liked": response["liked_total"],
            "view": response["view_times"],
        }
        before_data = self.file.file_load(path=data.CACHE_FILE_PATH, type="json")
        if before_data != {}:
            self.tool_routine.print_changes(
                before_data=before_data,  # type: ignore
                after_data=user_data,
                data={
                    "fans": "粉丝",
                    "collected": "被收藏",
                    "liked": "被赞",
                    "view": "被预览",
                },
            )
        self.file.write(path=data.CACHE_FILE_PATH, text=user_data, type="dict")

    # 猜测手机号码(暴力枚举)
    def guess_phonenum(self, phonenum: str) -> int | None:
        for i in range(10000):
            guess = f"{i:04d}"  # 格式化为四位数，前面补零
            test_string = int(phonenum.replace("****", guess))
            print(test_string)
            if self.user_motion.verify_phone(test_string):
                return test_string
