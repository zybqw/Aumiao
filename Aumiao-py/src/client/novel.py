from typing import Literal

import src.app.acquire as Acquire


class Obtain:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取小说分类列表
    def get_novel_categories(self):
        response = self.acquire.send_request(url="/api/fanfic/type", method="get")
        return response.json()

    # 获取小说列表
    def get_novel_list(
        self,
        method: Literal["all", "recommend"],
        sort_id: Literal[0, 1, 2, 3],
        type_id: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        status: Literal[0, 1, 2],
        page: int = 1,
        limit: int = 20,
    ):
        # sort_id: 0:默认排序 1:最多点击 2:最多收藏 3:最近更新
        # type_id: 0:不限 1:魔法 2:科幻 3:游戏 4:推理 5:治愈 6:冒险 7:日常 8:校园 9:格斗 10:古风 11:恐怖
        # status: 0:全部 1:连载中 2:已完结
        # method: all:全部 recommend:推荐
        # 经测试recommend返回数据不受params影响 recommend TODO: 待确认
        params = {
            "sort_id": sort_id,
            "type_id": type_id,
            "status": status,
            "page": page,
            "limit": limit,
        }
        # params中的type_id与fanfic_type_id可互换
        response = self.acquire.send_request(
            url=f"/api/fanfic/list/{method}", method="get", params=params
        )
        return response.json()

    # 获取收藏的小说列表
    def get_novel_collection(self, page: int = 1, limit: int = 10):
        params = {"page": page, "limit": limit}
        response = self.acquire.send_request(
            url="/web/fanfic/collection",
            method="get",
            params=params,
        )
        return response.json()
