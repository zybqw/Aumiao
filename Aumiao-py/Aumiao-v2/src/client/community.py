from typing import Any, Dict, List

import src.app.acquire as Acquire
import src.app.tool as Tool


class Community:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()
        self.tool = Tool.CodeMaoProcess()

    # 获取随机昵称
    def get_name_random(self) -> str:
        response = self.acquire.send_request(
            method="get",
            url="/api/user/random/nickname",
        )
        return response.json()["data"]["nickname"]

    # 获取新回复
    def get_new_replies(self) -> List[Dict[str, Any]]:
        _dict = []
        while True:
            record = self.send_request(
                url="/web/message-record/count",
                method="get",
            )
            reply_num = record.text.json()[0]["count"]
            if reply_num == 0:
                break
            list_num = sorted([5, reply_num, 200])[1]
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": list_num,
            }
            response = self.send_request(
                url="/web/message-record",
                method="get",
                params=params,
            )
            _dict.extend(response.json()["items"][:reply_num])
        return _dict
