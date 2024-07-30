import json

import src.app.acquire as acquire


class Obtain:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    # 获取工作室简介(简易,需登录工作室成员账号)
    def get_shops_simple(self):
        response = self.acquire.send_request(url="/web/work_shops/simple", method="get")
        result = response.json()["work_shop"]  # type: ignore
        return result

    # 获取工作室简介
    def get_shop_details(self, id: str) -> dict:
        response = self.acquire.send_request(url=f"/web/shops/{id}", method="get")

        return response.json()  # type: ignore

    # 获取工作室列表的函数
    def get_shops(
        self,
        level: int = 4,
        limit: int = 14,
        works_limit: int = 4,
        offset: int = 0,
        sort: str | None = None,
    ):  # 不要问我limit默认值为啥是14，因为api默认获取14个
        # sort可以不填,参数为-latest_joined_at,-created_at这两个可以互换位置，但不能填一个
        params = {
            "level": level,
            "works_limit": works_limit,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        shops = self.acquire.fetch_all_data(
            url="/web/work-shops/search",
            params=params,
            total_key="total",
            data_key="items",
        )
        return shops

    # 获取工作室成员
    def get_shops_members(self, id: int, limit: int = 40, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        members = self.acquire.fetch_all_data(
            url=f"https://api.codemao.cn/web/shops/{id}/users",
            params=params,
            total_key="total",
            data_key="items",
        )
        return members


class Motion:

    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    # 更新工作室简介
    def update_shop_details(
        self, description: str, id: str, name: str, preview_url: str
    ) -> bool:
        response = self.acquire.send_request(
            url="/web/work_shops/update",
            method="post",
            data=json.dumps(
                {
                    "description": description,
                    "id": id,
                    "name": name,
                    "preview_url": preview_url,
                }
            ),
        )
        return response.status_code == 200  # type: ignore
