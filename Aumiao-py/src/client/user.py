import json
from typing import Literal

import src.app.acquire as Acquire


class Obtain:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取某人账号信息
    def get_user_detials(self, user_id: str) -> dict:
        response = self.acquire.send_request(
            method="get", url=f"/api/user/info/detail/{user_id}"
        )
        return response.json()

    # 获取用户荣誉
    def get_user_honor(self, user_id: str) -> dict:
        params = {"user_id": user_id}
        response = self.acquire.send_request(
            url="/creation-tools/v1/user/center/honor",
            method="get",
            params=params,
        )

        return response.json()

    # 获取用户精确数据
    def get_user_business(self, user_id: str) -> dict:
        params = {"user_id": user_id}
        response = self.acquire.send_request(
            url="/nemo/v2/works/business/total", method="get", params=params
        )
        return response.json()

    # 获取某人账号信息(简略)
    def get_user_info(self, user_id: str) -> dict:
        params = {"user_id": user_id}
        response = self.acquire.send_request(
            method="get", url="/nemo/v2/user/dynamic/info", params=params
        )
        return response.json()

    # 获取账户信息(详细)
    def get_data_details(self) -> dict:
        response = self.acquire.send_request(
            method="get",
            url="/web/users/details",
        )
        return response.json()

    # 获取账户信息(简略)
    def get_data_info(self) -> dict:
        response = self.acquire.send_request(
            method="get",
            url="/web/users/info",
        )

        return response.json()

    # 获取账户信息
    def get_data_profile(self):
        response = self.acquire.send_request(
            method="get", url="/tiger/v3/web/accounts/profile"
        )
        return response.json()

    # 获取账户安全信息
    def get_data_privacy(self):
        response = self.acquire.send_request(
            method="get", url="/tiger/v3/web/accounts/privacy"
        )
        return response.json()

    # 获取账户信息
    def get_data_tiger(self):
        response = self.acquire.send_request(url="/tiger/user", method="get")
        return response.json()

    # 获取用户点赞，再创作，收藏分
    def get_data_score(self):
        response = self.acquire.send_request(
            url="/nemo/v3/user/grade/details", method="get"
        )
        return response.json()

    # 获取用户等级
    def get_data_level(self):
        response = self.acquire.send_request(
            url="/nemo/v3/user/level/info", method="get"
        )
        return response.json()

    # 获取用户姓名
    def get_data_name(self):
        response = self.acquire.send_request(
            url="/api/v2/pc/lesson/user/info", method="get"
        )
        return response.json()

    # 获取个人作品列表的函数
    def get_user_works_web(
        self, user_id: str, type: Literal["newest", "hot"] = "newest"
    ) -> list[dict[str, str | int]]:
        params = {
            "type": type,
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

    # 获取用户KN或nemo作品
    def get_user_works_nemo(
        self, method: Literal["published", "total"], type: Literal["KN", "nemo"]
    ):
        extra_url = "nemo" if type == "nemo" else "neko"
        if method == "published":
            url = (
                f"https://api-creation.codemao.cn/{extra_url}/works/list/user/published"
            )
        elif method == "total":
            url = f"https://api-creation.codemao.cn/{extra_url}/works/v2/list/user"
        params = {"offset": 0, "limit": 15}
        works = self.acquire.fetch_all_data(url=url, params=params, data_key="items")
        return works

    # 获取粉丝列表
    def get_user_fans(self, user_id: str) -> list[dict[str, str]]:
        params = {
            "user_id": user_id,
            "offset": 0,
            "limit": 15,
        }
        fans = self.acquire.fetch_all_data(
            url="/creation-tools/v1/user/fans",
            params=params,
            total_key="total",
            data_key="items",
        )
        return fans

    # 获取关注列表
    def get_user_follows(self, user_id: str) -> list[dict[str, str]]:
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


class Motion:

    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 设置登录用户名(实验性功能)
    def set_username(self, username):
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/username",
            method="patch",
            data=json.dumps({"username": username}),
        )
        return response.status_code

    # 验证手机号
    def verify_phone(self, phone_num: int):
        params = {"phone_number": phone_num}
        response = self.acquire.send_request(
            url="/web/users/phone_number/is_consistent", method="get", params=params
        )
        return response.json()

    # 修改密码
    def modify_password(self, old_password: str, new_password: str):
        data = json.dumps(
            {
                "old_password": old_password,
                "password": new_password,
                "confirm_password": new_password,
            }
        )
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/password",
            method="patch",
            data=data,
        )
        return response.status_code == 204

    # 修改手机号(获取验证码)
    def modify_phonenum_captcha(self, old_phonenum: int, new_phonenum: int) -> bool:
        data = json.dumps(
            {"phone_number": new_phonenum, "old_phone_number": old_phonenum}
        )
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/captcha/phone/change",
            method="post",
            data=data,
        )
        return response.status_code == 204

    # 修改手机号
    def modify_phonenum(self, captcha: int, phonenum: int) -> bool:
        data = json.dumps({"phone_number": phonenum, "captcha": captcha})
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/phone/change",
            method="patch",
            data=data,
        )
        return response.json()
