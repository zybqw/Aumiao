import json
from typing import Any, Dict, List, Optional

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

    # 获取新回复(传入参数就获取前*个回复,若没传入就获取新回复数量, 再获取新回复数量个回复)
    def get_replies(self, limit: int = 0) -> List[Dict[str, Any]]:
        _list = []
        record = self.acquire.send_request(
            url="/web/message-record/count",
            method="get",
        )
        reply_num = record.json()[0]["count"]
        if reply_num == limit == 0:
            return [{}]
        result_num = reply_num if limit == 0 else limit
        while True:
            list_num = sorted([5, result_num, 200])[1]
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": list_num,
            }
            # 获取前*个回复
            response = self.acquire.send_request(
                url="/web/message-record",
                method="get",
                params=params,
            )
            _list.extend(response.json()["items"][:result_num])
            result_num -= list_num
            if result_num <= 0:
                break
        return _list

    # 清除邮箱红点
    def clear_redpoint(self) -> bool:
        item = 0
        query_types = ["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"]
        while True:
            # 检查是否所有消息类型的红点数为0
            record = self.acquire.send_request(
                url="/web/message-record/count",
                method="get",
            )
            print(record)
            counts = [record.json()[i]["count"] for i in range(3)]
            if all(count == 0 for count in counts):
                return True  # 所有消息类型处理完毕

            # 如果还有未处理的消息,按类型查询并清理
            params = {
                "query_type": "ANYTHING",
                "limit": 200,
                "offset": item,
            }
            responses = {}
            for query_type in query_types:
                params["query_type"] = query_type
                response = self.client.send_request(
                    url="/web/message-record",
                    method="get",
                    params=params,
                )
                responses[query_type] = response.status_code
            if any(status != 200 for status in responses.values()):
                return False
            item += 200

    # 关注的函数
    def follow_work(self, user_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/nemo/v2/user/{user_id}/follow",
            method="post",
            data=json.dumps({}),
        )

        return response.status_code == 204

    # 收藏的函数
    def collection_work(self, work_id: int) -> bool:
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/{work_id}/collection",
            method="post",
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 对某个作品进行点赞的函数
    def like_work(self, work_id: int) -> bool:
        # 对某个作品进行点赞
        response = self.acquire.send_request(
            url=f"/nemo/v2/works/{work_id}/like",
            method="post",
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

    # 登录函数, 处理登录逻辑并保存登录状态
    def login(
        self,
        method: str = "password",
        identity: str | int = None,
        password: Any = None,
        cookies: Any = None,
    ) -> Optional[str]:
        if method == "password":
            # cookies = utils.dict_from_cookiejar(response.cookies)

            #   soup = BeautifulSoup(
            #       send_request("https://shequ.codemao.cn", "get").text,
            #       "html.parser",
            #   )
            #   见https://api.docs.codemao.work/user/login?id=pid
            #   pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
            pid = "65edCTyg"
            response = self.acquire.send_request(
                url="/tiger/v3/web/accounts/login",
                method="post",
                data=json.dumps(
                    {
                        "identity": identity,
                        "password": password,
                        "pid": pid,
                    }
                ),
            )
        elif method == "cookie":
            try:
                cookie_dict = dict([item.split("=", 1) for item in cookies.split("; ")])
            except (KeyError, ValueError) as err:
                print(f"表达式输入不合法 {err}")
                return False
            response = self.acquire.send_request(
                url="/nemo/v2/works/174408420/like",
                method="post",
                data=json.dumps({}),
                headers={**self.HEADERS, "cookie": cookie_dict},
            )
        if response.status_code == 200:
            self.acquire.update_cookie(response.cookies)  # 确保cookies被更新
            return True
        elif response.status_code == 403:
            return "Wrong"
        else:
            print(f"登录失败惹,错误码: {response.status_code}")
            return False

    # 获取作品
    def get_works(self, method: str, limit: int, offset: int = 0):
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
        _dict = response.json()
        result = self.tool.process_reject(
            data=_dict["items"], exclude=["preview_url", "avatar_url"]
        )
        return result
