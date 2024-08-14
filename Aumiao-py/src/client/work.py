import json
from typing import Literal

import src.app.acquire as acquire
import src.app.tool as tool

select = Literal["post", "delete"]


class Motion:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    # 关注的函数
    def follow_work(self, user_id: int, method: select = "post") -> bool:
        response = self.acquire.send_request(
            url=f"/nemo/v2/user/{user_id}/follow",
            method=method,
            data=json.dumps({}),
        )

        return response.status_code == 204

    # 收藏的函数
    def collection_work(self, work_id: int, method: select = "post") -> bool:
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/{work_id}/collection",
            method=method,
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 对某个作品进行点赞的函数
    def like_work(self, work_id: int, method: select = "post") -> bool:
        # 对某个作品进行点赞
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/{work_id}/like",
            method=method,
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 对某个作品进行评论的函数
    def comment_work(self, comment, emoji, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment",
            method="post",
            data=json.dumps(
                {
                    "content": comment,
                    "emoji_content": emoji,
                }
            ),
        )
        return response.status_code == 201

    # 对某个作品举报
    def report_work(self, describe: str, reason: str, work_id: int):
        data = json.dumps(
            {
                "work_id": work_id,
                "report_reason": reason,
                "report_describe": describe,
            }
        )
        response = self.acquire.send_request(
            url="https://api.codemao.cn/nemo/v2/report/work", method="post", data=data
        )
        return response.status_code == 200


class Obtain:

    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.tool = tool.CodeMaoProcess()

    # 获取评论区评论
    def get_work_comments(self, work_id: int):
        params = {"limit": 15, "offset": 0}
        comments = self.acquire.fetch_all_data(
            url=f"/creation-tools/v1/works/{work_id}/comments",
            params=params,
            total_key="page_total",
            data_key="items",
        )
        return comments

    # 获取作品信息
    def get_work_detail(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/creation-tools/v1/works/{work_id}",
            method="get",
        )
        return response.json()

    # 获取其他作品推荐
    def get_other_recommended(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/nemo/v2/works/web/{work_id}/recommended",
            method="get",
        )
        return response.json()

    # 获取作品信息(info)
    def get_work_info(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/api/work/info/{work_id}", method="get"
        )
        return response.json()

    # 获取作品标签
    def get_work_label(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/creation-tools/v1/work-details/work-labels?work_id={work_id}",
            method="get",
        )
        return response.json()

    # 获取作者更多作品
    def get_author_work(self, user_id: str):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/web/works/users/{user_id}", method="get"
        )
        return response.json()

    # 获取作品源码
    def get_work_source(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/source/public",
            method="get",
        )
        return response.json()

    # 获取最新或最热作品
    def discover_works_web(
        self, method: Literal["subject", "newest"], limit: int, offset: int = 0
    ):
        params = {"limit": limit, "offset": offset}
        if method == "subject":
            url = "/creation-tools/v1/pc/discover/subject-work"
        elif method == "newest":
            url = "/creation-tools/v1/pc/discover/newest-work"
        response = self.acquire.send_request(
            url=url,
            method="get",
            params=params,
        )  # 为防止封号,limit建议调大
        return response.json()

    # 获取推荐作品(nemo端)
    def discover_works_nemo(self):
        response = self.acquire.send_request(
            url="/creation-tools/v1/home/discover", method="get"
        )
        return response.json()

    # 获取用户KN或nemo作品
    def get_user_nemo(
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

    # 获取nemo端最新作品
    def get_new_nemo(
        self,
        type: Literal["course-work", "template", "original"],
        limit: int = 15,
        offset=0,
    ):
        params = {"limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url=f"/nemo/v3/newest/work/{type}/list", method="get", params=params
        )
        return response.json()
