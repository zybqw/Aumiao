from typing import Dict, List

import src.app.acquire as acquire
import src.app.tool as tool


class Work:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.tool = tool.CodeMaoProcess()

    # 获取评论区特定信息
    def get_comments_detail(
        self,
        work_id: int,
        method: str = "user_id",
    ) -> List[str] | List[Dict[str, int | bool]]:
        params = {"limit": 15, "offset": 0}
        comments = self.acquire.fetch_all_data(
            url=f"/creation-tools/v1/works/{work_id}/comments",
            params=params,
            total_key="page_total",
            data_key="items",
        )
        if method == "user_id":
            result = [item["user"]["id"] for item in comments]
        elif method == "comments":
            result = self.tool.process_reject(
                data=comments,
                reserve=["id", "content", "is_top"],
            )

        else:
            raise ValueError("不支持的请求方法")
        return result
