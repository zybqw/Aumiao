from typing import Literal

import src.app.acquire as acquire


class Obtain:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    # 获取多个帖子信息
    def get_posts_details(self, ids: int | list[int]):
        if isinstance(ids, int):
            params = {"ids": ids}
        elif isinstance(ids, list):
            params = {"ids": ",".join(map(str, ids))}
        response = self.acquire.send_request(
            url="/web/forums/posts/all", method="get", params=params
        )
        return response.json()

    # 获取单个帖子信息
    def get_single_post_details(self, id: int):
        response = self.acquire.send_request(
            url=f"/web/forums/posts/{id}/details", method="get"
        )
        return response.json()

    # 获取帖子回复
    def get_post_replies(
        self, id: int, page: int = 1, limit: int = 10, sort: str = "-created_at"
    ):
        params = {"page": page, "limit": limit, "sort": sort}
        replies = self.acquire.fetch_all_data(
            url=f"/web/forums/posts/{id}/replies",
            params=params,
            total_key="total",
            data_key="items",
            method="page",
            args={"amount": "limit", "remove": "page"},
        )
        return replies

    # 获取我的帖子或回复的帖子
    def get_post_mine(
        self,
        method: Literal["created", "replied"],
        page: int = 1,
        limit: int = 20,
    ):
        params = {"page": page, "limit": limit}
        posts = self.acquire.fetch_all_data(
            url=f"/web/forums/posts/mine/{method}",
            params=params,
            data_key="items",
            method="page",
            args={"amount": "limit", "remove": "page"},
        )
        return posts

    # 获取论坛帖子各个栏目
    def get_post_categories(self):
        response = self.acquire.send_request(
            url="/web/forums/boards/simples/all", method="get"
        )
        return response.json()

    # 获取社区所有热门帖子
    def get_hot_posts(self):
        response = self.acquire.send_request(
            url="/web/forums/posts/hots/all", method="get"
        )
        return response.json()

    # 获取论坛顶部公告
    def get_top_notice(self, limit: int = 4):
        params = {"limit": limit}
        response = self.acquire.send_request(
            url="/web/forums/notice-boards", method="get", params=params
        )
        return response.json()

    # 获取论坛本周精选帖子 TODO: 待完善
    def get_key_content(
        self, content_key: Literal["forum.index.top.recommend"], limit: int = 4
    ):
        params = {"content_key": content_key, "limit": limit}
        response = self.acquire.send_request(
            url="/web/contents/get-key", method="get", params=params
        )
        return response.json()

    # 获取社区精品合集帖子
    def get_selection_posts(self, limit: int = 20, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url="/web/forums/posts/selections",
            method="get",
            params=params,
        )
        return response.json()

    # 获取社区求帮助帖子
    def get_help_posts(self, limit: int = 20, page: int = 1):
        params = {"limit": limit, "page": page}
        response = self.acquire.send_request(
            url="/web/forums/boards/posts/ask-help",
            method="get",
            params=params,
        )
        return response.json()
