from typing import Dict, List

import src.app.acquire as Acquire


class User:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取某人账号信息
    def get_user_data(self, user_id: str) -> Dict:
        response = self.acquire.send_request(
            method="get", url=f"/api/user/info/detail/{user_id}"
        )

        return response.json()["data"]["userInfo"]

    # 获取账户信息(详细)
    def get_data_details(self) -> Dict:
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

    # 获取账户信息(简略)
    def get_data_info(self) -> Dict:
        response = self.acquire.send_request(
            method="get",
            url="/web/users/info",
        )

        return response.json()

    # 获取用户荣誉
    def get_user_honor(self, user_id: str) -> Dict:
        params = {"user_id": user_id}
        response = self.acquire.send_request(
            url="/creation-tools/v1/user/center/honor",
            method="get",
            params=params,
        )

        return response.json()

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
        return works

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
        return fans

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
        return follows
