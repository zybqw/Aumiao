import json
from typing import Literal

import src.base.acquire as acquire
import src.base.tool as tool

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
    def comment_work(
        self, comment, emoji, work_id: int, return_data: bool = False
    ) -> bool | dict:
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
        return response.json() if return_data else response.status_code == 201

    # 对某个作品下评论进行回复
    def reply_work(
        self,
        comment,
        work_id: int,
        comment_id: int,
        parent_id: int = 0,
        return_data: bool = False,
    ) -> bool | dict:
        data = json.dumps({"parent_id": parent_id, "content": comment})
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}/reply",
            method="post",
            data=data,
        )
        return response.json() if return_data else response.status_code == 201

    # 删除作品某个评论或评论的回复（评论和回复都会分配一个唯一id）
    def del_comment_work(self, work_id: int, comment_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}",
            method="delete",
        )
        return response.status_code == 204

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
            url="/nemo/v2/report/work", method="post", data=data
        )
        return response.status_code == 200

    # 设置某个评论置顶
    def set_comment_top(
        self,
        method: Literal["put", "delete"],
        work_id: int,
        comment_id: int,
        return_data: bool = False,
    ) -> bool:
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}/top",
            method=method,
            data=json.dumps({}),
        )
        return response.json() if return_data else response.status_code == 204

    # 点赞作品的评论
    def like_comment_work(self, work_id: int, comment_id: int, method: select = "post"):
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}/liked",
            method=method,
            data=json.dumps({}),
        )
        return response.status_code == 201

    # 举报作品的评论
    def report_comment_work(self, work_id: int, comment_id: int, reason: str):
        data = json.dumps(
            {
                "comment_id": comment_id,
                "report_reason": reason,
            }
        )
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/comment/report",
            method="post",
            data=data,
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
            url=f"/creation-tools/v1/works/{work_id}",
            method="get",
        )
        return response.json()

    # 获取其他作品推荐
    def get_other_recommended(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/web/{work_id}/recommended",
            method="get",
        )
        return response.json()

    # 获取作品信息(info)
    def get_work_info(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/api/work/info/{work_id}", method="get"
        )
        return response.json()

    # 获取作品标签
    def get_work_label(self, work_id: int):
        params = {"work_id": work_id}
        response = self.acquire.send_request(
            url="/creation-tools/v1/work-details/work-labels",
            method="get",
            params=params,
        )
        return response.json()

    # 获取作者更多作品
    def get_author_work(self, user_id: str):
        response = self.acquire.send_request(
            url=f"/web/works/users/{user_id}", method="get"
        )
        return response.json()

    # 获取作品源码
    def get_work_source(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}/source/public",
            method="get",
        )
        return response.json()

    # 获取最新作品
    def discover_works_new_web(self, limit: int, offset: int = 0, origin: bool = False):
        extra_params = {"work_origin_type": "ORIGINAL_WORK"} if origin else {}
        params = {**extra_params, "limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url="/creation-tools/v1/pc/discover/newest-work",
            method="get",
            params=params,
        )  # 为防止封号,limit建议调大
        return response.json()

    # 获取最新或最热作品
    def discover_works_subject_web(
        self, limit: int, offset: int = 0, subject_id: int = 0
    ):
        extra_params = {"subject_id": subject_id} if subject_id else {}
        params = {**extra_params, "limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url="/creation-tools/v1/pc/discover/subject-work",
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

    # 获取nemo端最新作品
    def discover_works_new_nemo(
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

    # 获取随机作品主题
    def get_subject_random_nemo(self) -> list[int]:
        response = self.acquire.send_request(
            url="/nemo/v3/work-subject/random", method="get"
        )
        return response.json()

    # 获取作品主题介绍
    def get_subject_info_nemo(self, id: int):
        response = self.acquire.send_request(
            url=f"/nemo/v3/work-subject/{id}/info", method="get"
        )
        return response.json()

    # 获取作品主题下作品
    def get_subject_work_nemo(self, id: int, limit: int = 15, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url=f"/nemo/v3/work-subject/{id}/works", method="get", params=params
        )
        return response.json()
