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
        self, work_id: int, comment, emoji=None, return_data: bool = False
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

    # 将一个作品设置为协作作品
    def set_coll_work(self, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"https://socketcoll.codemao.cn/coll/kitten/{work_id}",
            method="post",
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 删除一个未发布的作品
    def del_work(self, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"https://api-creation.codemao.cn/kitten/common/work/{work_id}/temporarily",
            method="delete",
        )
        return response.status_code == 200

    # 取消发布一个已发布的作品
    def unpublish_work(self, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/tiger/work/{work_id}/unpublish",
            method="patch",
            data=json.dumps({}),
        )
        return response.status_code == 204

    # 取消发布一个已发布的作品
    def unpublish_work_web(self, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/web/works/r2/unpublish/{work_id}",
            method="put",
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 获取回收站作品列表
    def get_recycle_kitten_works(
        self,
        version_no: Literal["KITTEN_V3", "KITTEN_V4"],
        limit: int = 30,
        offset: int = 0,
        work_status: str = "CYCLED",
    ):
        params = {
            "limit": limit,
            "offset": offset,
            "version_no": version_no,
            "work_status": work_status,
        }
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/tiger/work/recycle/list",
            method="get",
            params=params,
        )
        return response.json()

    # 获取回收站海龟编辑器作品列表
    def get_recycle_wood_works(
        self,
        limit: int = 30,
        offset: int = 0,
        language_type: int = 0,
        work_status: str = "CYCLED",
        published_status: str = "undefined",
    ):
        params = {
            "limit": limit,
            "offset": offset,
            "language_type": language_type,
            "work_status": work_status,
            "published_status": published_status,
        }
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/wood/comm/work/list",
            method="get",
            params=params,
        )
        return response.json()

    # 获取代码岛回收站作品列表
    def get_recycle_box_works(
        self,
        limit: int = 30,
        offset: int = 0,
        work_status: str = "CYCLED",
    ):
        params = {
            "limit": limit,
            "offset": offset,
            "work_status": work_status,
        }
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/box/v2/work/list",
            method="get",
            params=params,
        )
        return response.json()

    # 获取回收站小说列表
    def get_recycle_fanfic_works(
        self,
        limit: int = 30,
        offset: int = 0,
        fiction_status: str = "CYCLED",
    ):
        params = {
            "limit": limit,
            "offset": offset,
            "fiction_status": fiction_status,
        }
        response = self.acquire.send_request(
            url="https://api.codemao.cn/web/fanfic/my/new",
            method="get",
            params=params,
        )
        return response.json()

    # 删除回收站作品
    def del_recycle_kitten_works(self):
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/tiger/work/recycle/permanently",
            method="delete",
        )

        return response.status_code == 204


class Obtain:

    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.tool = tool.CodeMaoProcess()

    # 获取评论区评论
    def get_work_comments(self, work_id: int, limit: int = 15):
        params = {"limit": 15, "offset": 0}
        comments = self.acquire.fetch_data(
            url=f"/creation-tools/v1/works/{work_id}/comments",
            params=params,
            total_key="page_total",
            data_key="items",
            limit=limit,
        )
        return comments

    # 获取作品信息
    def get_work_detail(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/creation-tools/v1/works/{work_id}",
            method="get",
        )
        return response.json()

    # 获取kitten作品信息
    def get_kitten_work_detail(self, work_id: int):
        response = self.acquire.send_request(
            url=f"https://api-creation.codemao.cn/kitten/work/detail/{work_id}",
            method="get",
        )
        return response.json()

    # 获取其他作品推荐_web端
    def get_other_recommended_web(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/web/{work_id}/recommended",
            method="get",
        )
        return response.json()

    # 获取其他作品推荐_nemo端
    def get_other_recommended_nemo(self, work_id: int):
        params = {"work_id": work_id}
        response = self.acquire.send_request(
            url="/nemo/v3/work-details/recommended/list",
            method="get",
            params=params,
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

    # 获取所有kitten作品标签
    def get_kitten_work_label(self):
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/kitten/work/labels", method="get"
        )
        return response.json()

    # 获取所有kitten默认封面
    def get_kitten_default_cover(self):
        response = self.acquire.send_request(
            url="https://api-creation.codemao.cn/kitten/work/cover/defaultCovers",
            method="get",
        )
        return response.json()

    # 检查作品名称是否可用
    def check_work_name(self, name: str, work_id: int):
        params = {"name": name, "work_id": work_id}
        response = self.acquire.send_request(
            url="/tiger/work/checkname", method="get", params=params
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
        type: Literal["course-work", "template", "original", "fork"],
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

    # 获取协作邀请码
    def get_coll_code(self, work_id: int, method: Literal["get", "delete"] = "get"):
        response = self.acquire.send_request(
            url=f"https://socketcoll.codemao.cn/coll/kitten/collaborator/code/{work_id}",
            method=method,
        )
        return response.json()

    # 获取协作者列表
    def get_coll_list(self, work_id: int):
        params = {"current_page": 1, "page_size": 100}
        list = self.acquire.fetch_data(
            url=f"https://socketcoll.codemao.cn/coll/kitten/collaborator/{work_id}",
            params=params,
            total_key="data.total",
            data_key="data.items",
            method="page",
            args={"amount": "current_page", "remove": "page_size"},
        )
        return list

    # 获取作品再创作情况_web端
    def get_recreate_info_web(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/tiger/work/tree/{work_id}",
            method="get",
        )
        return response.json()

    # 获取作品再创作情况_nemo端
    def get_recreate_info_nemo(self, work_id: int):
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/root/{work_id}",
            method="get",
        )
        return response.json()
