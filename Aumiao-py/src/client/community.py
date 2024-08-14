import json
import uuid
from typing import Literal

import src.app.acquire as Acquire
import src.app.tool as Tool


# 编程猫所有api中若包含v2等字样，表示第几版本，同样比它低的版本也可使用
class Login:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()
        self.tool_process = Tool.CodeMaoProcess()

    # 密码登录函数
    def login_password(
        self,
        identity: str,
        password: str,
        pid: str = "65edCTyg",
    ) -> str | None:

        # cookies = utils.dict_from_cookiejar(response.cookies)

        #   soup = BeautifulSoup(
        #       send_request("https://shequ.codemao.cn", "get").text,
        #       "html.parser",
        #   )
        #   见https://api.docs.codemao.work/user/login?id=pid
        #   pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
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
        self.check_login(response)

    # cookie登录
    def login_cookie(self, cookies: str) -> None | bool:

        try:
            dict([item.split("=", 1) for item in cookies.split("; ")])
            # 检查是否合规,不能放到headers中
        except (KeyError, ValueError) as err:
            print(f"表达式输入不合法 {err}")
            return False
        response = self.acquire.send_request(
            url="/nemo/v2/works/174408420/like",
            method="post",
            data=json.dumps({}),
            headers={**self.acquire.HEADERS, "cookie": cookies},
        )
        self.check_login(response)

    # token登录(毛毡最新登录方式)
    def login_token(self, identity: str, password: str, pid: str = "65edCTyg"):
        timestamp = Obtain().get_timestamp()["data"]
        response = self.get_login_ticket(
            identity=identity, timestamp=timestamp, pid=pid
        )
        ticket = response["ticket"]
        response = self.get_login_security(
            identity=identity, password=password, ticket=ticket, pid=pid
        )

    # 返回完整鉴权cookie
    def get_login_auth(self, token):
        # response = src.app_acquire.send_request(url="https://shequ.codemao.cn/",method="get",)
        # aliyungf_tc = response.cookies.get_dict()["aliyungf_tc"]
        uuid_ca = uuid.uuid1()
        token_ca = {"authorization": token, "__ca_uid_key__": str(uuid_ca)}
        cookie_str = self.tool_process.process_cookie(token_ca)
        headers = {**self.acquire.HEADERS, "cookie": cookie_str}
        response = self.acquire.send_request(
            method="get", url="/web/users/details", headers=headers
        )
        _auth = response.cookies.get_dict()
        auth_cookie = {**token_ca, **_auth}
        return auth_cookie

    # 检查并保存登录状态
    def check_login(self, response, cookie=None):
        if response.status_code == 200:
            up_cookie = cookie if cookie else response.cookies
            self.acquire.update_cookie(up_cookie)  # 确保cookies被更新
            return True
        elif response.status_code == 403:
            return "Wrong"
        else:
            print(f"登录失败惹,错误码: {response.status_code}")
            return False

    # 退出登录
    def logout(self):
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/logout", method="post", data=json.dumps({})
        )
        return response.status_code == 204

    # 登录信息
    def get_login_security(
        self,
        identity: str,
        password: str,
        ticket: str,
        pid: str = "65edCTyg",
        agreement_ids: list = [-1],
        cookies_ali: dict = {"ca": "", "acw_tc": "", "aliyungf_tc": ""},
    ):
        data = json.dumps(
            {
                "identity": identity,
                "password": password,
                "pid": pid,
                "agreement_ids": agreement_ids,
            }
        )
        _ca = {
            "__ca_uid_key__": str(cookies_ali["ca"]),
            "acw_tc": cookies_ali["acw_tc"],
            "aliyungf_tc": cookies_ali["aliyungf_tc"],
        }
        cookie_str = self.tool_process.process_cookie(_ca)
        headers_auth = {**self.acquire.HEADERS, "cookie": cookie_str}
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/login/security",
            method="post",
            data=data,
            headers={**headers_auth, "x-captcha-ticket": ticket},
        )
        self.check_login(response)
        return response.json()

    #
    # 登录ticket获取
    def get_login_ticket(
        self,
        identity,
        timestamp: int,
        cookies_ca=None,
        scence=None,
        pid: str = "65edCTyg",
        deviced=None,
    ):
        _ca = {"__ca_uid_key__": str(cookies_ca)}
        cookie_str = self.tool_process.process_cookie(_ca)
        headers = {**self.acquire.HEADERS, "cookie": cookie_str}
        data = json.dumps(
            {
                "identity": identity,
                "scene": scence,
                "pid": pid,
                "deviceId": deviced,
                "timestamp": timestamp,
            }
        )
        response = self.acquire.send_request(
            url="https://open-service.codemao.cn/captcha/rule/v3",
            method="post",
            data=data,
            headers=headers,
        )
        return response.json()


class Obtain:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取随机昵称
    def get_name_random(self) -> str:
        response = self.acquire.send_request(
            method="get",
            url="/api/user/random/nickname",
        )
        return response.json()["data"]["nickname"]

    # 获取新消息数量
    def get_message_count(self, method: Literal["web", "nemo"]):
        if method == "web":
            url = "/web/message-record/count"
        elif method == "nemo":
            url = "/nemo/v2/user/message/count"
        else:
            raise ValueError("不支持的方法")
        record = self.acquire.send_request(
            url=url,
            method="get",
        )
        return record.json()

    # 获取回复
    def get_replies(
        self,
        type: Literal["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"],
        limit: int = 15,
        offset: int = 0,
    ):
        params = {"query_type": type, "limit": limit, "offset": offset}
        # 获取前*个回复
        response = self.acquire.send_request(
            url="/web/message-record",
            method="get",
            params=params,
        )
        return response.json()

    # 获取nemo消息
    def get_nemo_message(self, method: Literal["fork", "like"]):
        extra_url = 1 if method == "like" else 3
        url = f"/nemo/v2/user/message/{extra_url}"
        response = self.acquire.send_request(url=url, method="get")
        return response.json()

    # 清除邮箱红点
    def all_read(
        self, query_types: list[Literal["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"]]
    ) -> bool:
        offset = 0
        while True:
            record = self.get_message_count(method="web")
            type_to_count = {item["query_type"]: item["count"] for item in record}
            if all(type_to_count.get(type, 0) == 0 for type in query_types):
                return True  # 所有消息类型处理完毕
            # 如果还有未处理的消息,按类型查询并清理
            responses = {}
            for query_type in query_types:
                response = self.get_replies(type=query_type, limit=200, offset=offset)
                responses[query_type] = response.status_code
            if any(status != 200 for status in responses.values()):
                return False
            offset += 200

    # 获取点个猫更新
    def get_update_message(self):
        response = self.acquire.send_request(
            url="https://update.codemao.cn/updatev2/appsdk", method="get"
        )
        return response.json()

    # 获取时间戳
    def get_timestamp(self):
        response = self.acquire.send_request(
            url="/coconut/clouddb/currentTime", method="get"
        )
        return response.json()

    # 获取推荐头图
    def get_banner(self, type: str = "FLOAT_BANNER"):
        response = self.acquire.send_request(
            url=f"https://api.codemao.cn/web/banners/all?type={type}", method="get"
        )
        return response.json()

    # 获取举报类型
    def get_report_reason(self):
        response = self.acquire.send_request(
            url="https://api.codemao.cn/web/reports/reasons/all", method="get"
        )
        return response.json()

    # 未知
    def get_nemo_config(self) -> str:
        response = self.acquire.send_request(
            url="https://nemo.codemao.cn/config", method="get"
        )
        return response.json()

    # 获取编程猫网络服务
    def get_client_config(self):
        response = self.acquire.send_request(
            url="https://player.codemao.cn/new/client_config.json", method="get"
        )
        return response.json()

    # 获取随机作品主题
    def get_subject_random(self) -> list[int]:
        response = self.acquire.send_request(
            url="/nemo/v3/work-subject/random", method="get"
        )
        return response.json()

    # 获取作品主题介绍
    def get_subject_info(self, id: int):
        response = self.acquire.send_request(
            url=f"/nemo/v3/work-subject/{id}/info", method="get"
        )
        return response.json()

    # 获取作品主题下作品
    def get_subject_work(self, id: int, limit: int = 15, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        response = self.acquire.send_request(
            url=f"/nemo/v3/work-subject/{id}/works", method="get", params=params
        )
        return response.json()
