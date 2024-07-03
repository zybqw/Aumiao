import src.app.acquire as Acquire
import src.app.tool as Tool
from typing import List, Dict


class User:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()
        self.tool = Tool.CodeMaoProcess()

    # 获取用户账号信息
    # (简略)
    def get_user_data(self, user_id: str) -> Dict:
        response = self.acquire.send_request(
            method="get", url=f"/api/user/info/detail/{user_id}"
        )
        result = self.tool.process_reject(
            data=response.json()["data"]["userInfo"],
            exclude=["work", "isFollowing"],
        )
        return result

    # (详细)
    def get_user_details(self) -> Dict:
        response = self.acquire.send_request(
            method="get",
            url="/web/users/details",
        )
        result = self.tool.process_reject(
            data=response.json(),
            reserve=[
                "id",
                "nickname",
                "description",
                "create_time",
                "author_level",
            ],
        )
        return result

    # 获取用户荣誉
    def get_user_honor(self, user_id: str) -> Dict:
        params = {"user_id": user_id}
        response = self.acquire.send_request(
            url="/creation-tools/v1/user/center/honor",
            method="get",
            params=params,
        )
        result = self.tool.process_reject(
            data=response.json(),
            exclude=[
                "avatar_url",
                "user_cover",
                "attention_status",
                "attention_total",
                "collect_times",
                "consume_level",
                "is_official_certification",
                "subject_id",
                "like_score",
                "collect_score",
                "fork_score",
                "head_frame_type",  # 以下四个为头像框
                "head_frame_fame",
                "head_frame_url",
                "small_head_frame_url",
            ],
        )
        return result

    # 获取个人作品列表的函数
    def get_user_works(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "type": "newest",
            "user_id": user_id,
            "offset": 0,
            "limit": 5,
        }
        works = self.acquire.fetch_all_data(
            url="/creation-tools/v2/user/center/work-list",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(works, reserve=["id", "work_name"])
        return result

    # 获取粉丝列表
    def get_user_fans(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "user_id": user_id,
            "offset": 0,
            "limit": 15,
        }
        fans = self.fetch_all_data(
            url="/creation-tools/v1/user/fans",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(fans, reserve=["id", "nickname"])
        return result

    # 获取关注列表
    def get_user_follows(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "user_id": user_id,
            "offset": 0,
            "limit": 15,
        }
        follows = self.acquire.fetch_all_data(
            url="/creation-tools/v1/user/followers",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(follows, reserve=["id", "nickname"])
        return result
