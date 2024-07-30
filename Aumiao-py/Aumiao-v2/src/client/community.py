import json
import uuid

import src.app.acquire as Acquire
import src.app.data as Data
import src.app.tool as Tool


class Login:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()
        self.data = Data.CodeMaoData()
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
            headers={**self.data.PROGRAM_DATA["HEADERS"], "cookie": cookies},
        )
        self.check_login(response)

    # token登录(毛毡最新登录方式)
    def login_token(self, identity: str, password: str):
        timestamp = Obtain().get_timestamp()["data"]
        response = self.get_login_ticket(identity=identity, timestamp=timestamp)
        ticket = response["ticket"]
        response = self.get_login_security(
            identity=identity, password=password, ticket=ticket
        )
        token = response["auth"]["token"]
        # src.client_community_login.logout()
        _auth = self.get_login_auth(token)
        cookie_str = self.tool_process.process_cookie(_auth)
        # 可以仅在cookie中填写authorization=token
        headers = {**self.data.PROGRAM_DATA["HEADERS"], "cookie": cookie_str}
        response = self.acquire.send_request(
            method="get", url="/web/users/details", headers=headers
        )
        self.check_login(response, _auth)
        # 可以不用填第二个参数，从而取消存储ca—uid这个cookie键值

    # 返回完整鉴权cookie
    def get_login_auth(self, token):
        # response = src.app_acquire.send_request(url="https://shequ.codemao.cn/",method="get",)
        # aliyungf_tc = response.cookies.get_dict()["aliyungf_tc"]
        uuid_ca = uuid.uuid1()
        token_ca = {"authorization": token, "__ca_uid_key__": str(uuid_ca)}
        cookie_str = self.tool_process.process_cookie(token_ca)
        headers = {**self.data.PROGRAM_DATA["HEADERS"], "cookie": cookie_str}
        response = self.acquire.send_request(
            method="get", url="/web/users/details", headers=headers
        )
        _auth = response.cookies.get_dict()  # type: ignore
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
        return response.status_code == 204  # type: ignore

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
        headers_auth = {**self.data.PROGRAM_DATA["HEADERS"], "cookie": cookie_str}
        response = self.acquire.send_request(
            url="/tiger/v3/web/accounts/login/security",
            method="post",
            data=data,
            headers={**headers_auth, "x-captcha-ticket": ticket},
        )
        return response.json()  # type: ignore

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
        headers = {**self.data.PROGRAM_DATA["HEADERS"], "cookie": cookie_str}
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
        return response.json()  # type: ignore


class Obtain:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取随机昵称
    def get_name_random(self) -> str:
        response = self.acquire.send_request(
            method="get",
            url="/api/user/random/nickname",
        )
        return response.json()["data"]["nickname"]  # type: ignore

    # 获取新回复(传入参数就获取前*个回复,若没传入就获取新回复数量, 再获取新回复数量个回复)
    def get_replies(self, limit: int = 0) -> list[dict[str, str | int]]:
        _list = []
        record = self.acquire.send_request(
            url="/web/message-record/count",
            method="get",
        )
        reply_num = record.json()[0]["count"]  # type: ignore
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
            _list.extend(response.json()["items"][:result_num])  # type: ignore
            result_num -= list_num
            if result_num <= 0:
                break
        return _list

    # 清除邮箱红点
    def all_read(self) -> bool:
        item = 0
        query_types = ["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"]
        while True:
            # 检查是否所有消息类型的红点数为0
            record = self.acquire.send_request(
                url="/web/message-record/count",
                method="get",
            )
            counts = [record.json()[i]["count"] for i in range(3)]  # type: ignore
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
                response = self.acquire.send_request(
                    url="/web/message-record",
                    method="get",
                    params=params,
                )
                responses[query_type] = response.status_code  # type: ignore
            if any(status != 200 for status in responses.values()):
                return False
            item += 200

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
        return response.json()  # type: ignore

    # 获取时间戳
    def get_timestamp(self):
        response = self.acquire.send_request(
            url="/coconut/clouddb/currentTime", method="get"
        )
        return response.json()  # type: ignore
