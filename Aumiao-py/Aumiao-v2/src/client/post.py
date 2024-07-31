import src.app.acquire as acquire


class Obtain:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    # 获取多个帖子信息
    def get_posts_details(self, ids: int | list):
        if isinstance(ids, int):
            params = {"ids": ids}
        elif isinstance(ids, list):
            params = {"ids": ",".join(map(str, ids))}
        response = self.acquire.send_request(
            url="/web/forums/posts/all", method="get", params=params
        )
        return response.json()

    # 获取单个帖子信息
    def get_single_details(self, id: int):
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
