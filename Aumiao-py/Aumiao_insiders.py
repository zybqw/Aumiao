import json
import os
import time
from typing import Any, Dict, List, Optional, Union

# 在获取任何数据时, 链接参数中的`offset`表示忽略前**个作品, `limit`获取之后的作品列表
# offset为非必选项, limit为必选项,大多数必须大于等于5, 小于等于200
# 获取某人作品列表limit无限制
# user_id为一串数字, 但api返回时返回类型为字符串, 故在爬虫中采用字符串类型

# 尝试导入requests库
try:
    import requests
    from requests.exceptions import (
        ConnectionError,
        HTTPError,
        RequestException,
        Timeout,
    )
except ModuleNotFoundError:
    # 提示用户未安装requests库,并询问安装位置
    print("检测到您未下载requests库,正在为您安装.")
    step = input(
        "如果安装了多个python版本,请输入要安装的位置(例如:3.x),否则直接回车跳过: "
    )
    if step.strip():
        # 如果用户指定了Python版本,按照指定的版本安装
        os.system(
            f"py -{step} -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple"
        )
    else:
        # 如果用户未指定版本,则尝试默认安装
        os.system("pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")

    # 尝试重新导入requests库
    try:
        import requests
        from requests.exceptions import (
            ConnectionError,
            HTTPError,
            RequestException,
            Timeout,
        )
    except ModuleNotFoundError:
        # 如果安装失败,则退出程序
        print("安装requests库失败,请手动安装后再运行程序.")
        exit(1)
session = requests.session()


class CodeMaoData:
    CONFIG_FILE_PATH: str = os.path.join(os.getcwd(), "CodeMaoData.json")

    def __init__(self):
        data = CodeMaoTool().file_load(self.CONFIG_FILE_PATH)
        self.BASE_URL = data["BASE_URL"]
        self.SLOGAN = data["SLOGAN"]
        self.HEADERS.update(data["HEADERS"])
        self.Data.update(data["Data"])

    SLOGAN = ""
    BASE_URL = ""
    HEADERS = {}
    Account = {
        "identity": " ",
        "password": " ",
        "id": " ",
        "nickname": " ",
        "create_time": " ",
        "author_level": " ",
        "description": " ",
    }
    # 实际使用的数据类
    Data = {
        "blackroom": [" "],
        "comments": [" "],
        "emojis": [" "],
        "answers": [" "],
        "ad": [" "],
        # ... (其他实际使用的内容, 如评论、表情等)
    }


class CodeMaoTool:
    def process_reject(
        self, data: List | Dict, reserve: List = None, exclude: List = None
    ) -> List | Dict:
        if reserve and exclude:
            raise ValueError(
                "请仅提供 'reserve' 或 'exclude' 中的一个参数,不要同时使用."
            )

        def filter_keys(item):
            if reserve is not None:
                return {key: value for key, value in item.items() if key in reserve}
            elif exclude is not None:
                return {key: value for key, value in item.items() if key not in exclude}

        if isinstance(data, list):
            return [filter_keys(item) for item in data]
        elif isinstance(data, dict):
            return filter_keys(data)
        else:
            raise ValueError("不支持的数据类型")

    # 通过点分隔的键路径从嵌套字典中获取值
    def get_by_path(self, data: Dict, path: str) -> Any:
        keys = path.split(".")
        value = data
        for key in keys:
            value = value.get(key, {})
        return value

    # 对评论内容进行处理的函数
    def process_shielding(self, content: str) -> str:
        content_bytes = [item.encode("UTF-8") for item in content]
        result = b"\xe2\x80\x8b".join(content_bytes).decode("UTF-8")
        return result

    # 时间戳转换为时间
    def process_timestamp(self, times: int) -> str:
        timeArray = time.localtime(times)
        StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return StyleTime

    # 从配置文件加载账户信息的函数
    def file_load(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    # 检查文件
    def check_file(self, path: str) -> bool:
        try:
            with open(path, "r"):
                return True
        except IOError:
            return False

    # 将文本写入到指定文件的函数
    def write(
        self,
        path: str,
        text: Union[str, Dict],
        type: str = "str",
        method: str = "w",
    ) -> None:
        with open(path, mode=method, encoding="utf-8") as file:
            if type == "str":
                file.write(text + "\n")
            elif type == "dict":
                file.write(json.dumps(text, ensure_ascii=False, indent=4))
            else:
                raise ValueError("不支持的写入方法")


class CodeMaoClient:
    def __init__(self) -> None:
        self.data = CodeMaoData()
        self.tool = CodeMaoTool()
        global session

    def send_request(
        self,
        url: str,
        method: str,
        params: Optional[Dict] = None,
        data: Any = None,
        headers: Dict = None,
    ) -> Optional[Any]:
        headers = headers or self.data.HEADERS
        url = f"{self.data.BASE_URL}{url}"
        try:
            response = session.request(
                method=method, url=url, headers=headers, params=params, data=data
            )
            response.raise_for_status()
            return response
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            print(response.json())
            print(f"网络请求异常: {err}")
            return None

    def fetch_all_data(
        self,
        url: str,
        params: Dict[str, any],
        total_key: str,
        data_key: str,
        method: str = "offset",
        args: Dict = {"limit": "limit", "offset": "offset"},
    ) -> List[Dict]:
        # 发送初始请求以获取总数
        initial_response = self.send_request(url=url, method="get", params=params)
        total_items = int(self.tool.get_by_path(initial_response.json(), total_key))
        items_per_page = params[args["limit"]]
        total_pages = (total_items // items_per_page) + (
            1 if total_items % items_per_page > 0 else 0
        )
        all_data = []

        # 遍历所有页面收集数据
        for page in range(total_pages):
            if method == "offset":
                params[args["offset"]] = page * items_per_page
            elif method == "page":
                params[args["offset"]] = page + 1 if page != total_pages else page
            response = self.send_request(url=url, method="get", params=params)
            all_data.extend(self.tool.get_by_path(response.json(), data_key))
        return all_data

    # 获取用户账号信息
    # (简略)
    def get_user_data(self, user_id: str) -> Dict:
        response = self.send_request(
            method="get", url=f"/api/user/info/detail/{user_id}"
        )
        result = self.tool.process_reject(
            data=response.json()["data"]["userInfo"],
            exclude=["work", "isFollowing"],
        )
        return result

    # (详细)
    def get_user_details(self) -> Dict:
        response = self.send_request(
            method="get",
            url="/web/users/details",
        )
        result = self.tool.process_reject(
            data=response.json(),
            reserve=[
                "id",
                "nickname",
                "description",
                "create_time",
                "author_level",
            ],
        )
        return result

    # 获取用户荣誉
    def get_user_honor(self, user_id: str) -> Dict:
        params = {"user_id": user_id}
        response = self.send_request(
            url="/creation-tools/v1/user/center/honor",
            method="get",
            params=params,
        )
        result = self.tool.process_reject(
            data=response.json(),
            exclude=[
                "avatar_url",
                "user_cover",
                "attention_status",
                "attention_total",
                "collect_times",
                "consume_level",
                "is_official_certification",
                "subject_id",
                "like_score",
                "collect_score",
                "fork_score",
                "head_frame_type",  # 以下四个为头像框
                "head_frame_fame",
                "head_frame_url",
                "small_head_frame_url",
            ],
        )
        return result

    # 获取个人作品列表的函数
    def get_user_works(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "type": "newest",
            "user_id": user_id,
            "offset": 0,
            "limit": 5,
        }
        works = self.fetch_all_data(
            url="/creation-tools/v2/user/center/work-list",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(works, reserve=["id", "work_name"])
        return result

    # 获取粉丝列表
    def get_user_fans(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "user_id": user_id,
            "offset": 0,
            "limit": 15,
        }
        fans = self.fetch_all_data(
            url="/creation-tools/v1/user/fans",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(fans, reserve=["id", "nickname"])
        return result

    # 获取关注列表
    def get_user_follows(self, user_id: str) -> List[Dict[str, str]]:
        params = {
            "user_id": user_id,
            "offset": 0,
            "limit": 15,
        }
        follows = self.fetch_all_data(
            url="/creation-tools/v1/user/followers",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(follows, reserve=["id", "nickname"])
        return result

    # 获取随机昵称
    def get_name_random(self) -> str:
        response = self.send_request(
            method="get",
            url="/api/user/random/nickname",
        )
        return response.json()["data"]["nickname"]

    # 获取作品
    def get_works(self, method: str, limit: int, offset: int = 0):
        params = {"limit": limit, "offset": offset}
        if method == "subject":
            url = "/creation-tools/v1/pc/discover/subject-work"
        elif method == "newest":
            url = "/creation-tools/v1/pc/discover/newest-work"
        response = self.send_request(
            url=url,
            method="get",
            params=params,
        )  # 为防止封号,limit建议调大
        _dict = response.json()
        result = self.tool.process_reject(
            data=_dict["items"], exclude=["preview_url", "avatar_url"]
        )
        return result

    # 获取评论区特定信息
    def get_comments_detail(
        self,
        work_id: int,
        method: str = "user_id",
    ) -> List[str] | List[Dict[str, int | bool]]:
        params = {"limit": 15, "offset": 0}
        comments = self.fetch_all_data(
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

    # 获取工作室简介(简易,需登录工作室成员账号)
    def get_shops_simple(self):
        response = self.send_request(url="/web/work_shops/simple", method="get")
        result = response.json()["work_shop"]
        return result

    # 获取工作室简介
    def get_shop_detials(self, id: str) -> Dict:
        response = self.send_request(url=f"/web/shops/{id}", method="get")
        result = self.tool.process_reject(
            data=response.json(),
            reserve=[
                "id",
                "shop_id",
                "name",
                "total_score",
                "preview_url",
                "description",
                "n_works",
                "n_views",
                "level",
            ],
        )
        return result

    # 更新工作室简介
    def update_shop_detials(
        self, description: str, id: str, name: str, preview_url: str
    ) -> bool:
        response = self.send_request(
            url="/web/work_shops/update",
            method="post",
            data=json.dumps(
                {
                    "description": description,
                    "id": id,
                    "name": name,
                    "preview_url": preview_url,
                }
            ),
        )
        return response.status_code == 200

    # 关注的函数
    def follow_work(self, user_id: int) -> bool:
        response = self.send_request(
            url=f"/nemo/v2/user/{user_id}/follow",
            method="post",
            data=json.dumps({}),
        )

        return response.status_code == 204

    # 收藏的函数
    def collection_work(self, work_id: int) -> bool:
        response = self.send_request(
            url=f"/nemo/v2/works/{work_id}/collection",
            method="post",
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 对某个作品进行点赞的函数
    def like_work(self, work_id: int) -> bool:
        # 对某个作品进行点赞
        response = self.send_request(
            url=f"/nemo/v2/works/{work_id}/like",
            method="post",
            data=json.dumps({}),
        )
        return response.status_code == 200

    # 对某个作品进行评论的函数
    def comment_work(self, comment, emoji, work_id: int) -> bool:
        response = self.send_request(
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

    # 获取工作室列表的函数
    def get_work_shops(
        self,
        level: int = 4,
        limit: int = 14,
        works_limit: int = 4,
        offset: int = 0,
        sort: str = None,
    ):  # 不要问我limit默认值为啥是14，因为api默认获取14个
        # sort可以不填,参数为-latest_joined_at,-created_at这两个可以互换位置，但不能填一个
        params = {
            "level": level,
            "works_limit": works_limit,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        shops = self.fetch_all_data(
            url="/web/work-shops/search",
            params=params,
            total_key="total",
            data_key="items",
        )
        result = self.tool.process_reject(
            data=shops,
            reserve=["id", "name", "description", "total_works"],
        )
        return result

    def clear_redpoint(self) -> bool:
        item = 0
        query_types = ["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"]
        while True:
            # 检查是否所有消息类型的红点数为0
            record = self.send_request(
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

    def get_posts_detials(self, ids: int | List):
        if isinstance(ids, int):
            params = {"ids": ids}
        elif isinstance(ids, List):
            params = {"ids": ",".join(map(str, ids))}
        response = self.send_request(
            url="/web/forums/posts/all", method="get", params=params
        )
        data = self.tool.process_reject(
            data=response.json(),
            reserve=["id", "title", "content", "created_at", "user"],
        )

        return data

    # 登录函数, 处理登录逻辑并保存登录状态
    def login(
        self,
        method: str = "password",
        identity: str | int = None,
        password: Any = None,
        cookies: Any = None,
    ) -> Optional[str]:
        self.cookie_pr = requests.utils.dict_from_cookiejar
        if method == "password":
            # cookies = utils.dict_from_cookiejar(response.cookies)

            #   soup = BeautifulSoup(
            #       send_request("https://shequ.codemao.cn", "get").text,
            #       "html.parser",
            #   )
            #   见https://api.docs.codemao.work/user/login?id=pid
            #   pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
            pid = "65edCTyg"
            response = self.send_request(
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
            response = self.send_request(
                url="/nemo/v2/works/174408420/like",
                method="post",
                data=json.dumps({}),
                headers={**self.data.HEADERS, "cookie": cookie_dict},
            )
        if response.status_code == 200:
            session.cookies.update(response.cookies)  # 确保cookies被更新
            return True
        elif response.status_code == 403:
            return "Wrong"
        else:
            print(f"登录失败惹,错误码: {response.status_code}")
            return False


class CodeMaoUnion:

    def __init__(self) -> None:
        self.tool = CodeMaoTool()
        self.client = CodeMaoClient()
        self.data = CodeMaoData()

    # 清除作品广告的函数
    def clear_ad(self, keys) -> bool:
        works_list = self.client.get_user_works(self.data.Account["id"])
        for item0 in works_list:
            comments = self.client.get_comments_detail(
                work_id=item0["id"], method="comments"
            )
            work_id = item0["id"]
            for item1 in comments:
                comment_id = item1["id"]
                content = item1["content"].lower()  # 转换小写
                if (
                    any(item2 in content for item2 in keys)
                    and not item1["is_top"]  # 取消置顶评论监测
                ):
                    print(
                        "在作品 {} 中发现广告: {} ".format(item0["work_name"], content)
                    )
                    response = self.client.send_request(
                        url=f"/creation-tools/v1/works/{work_id}/comment/{comment_id}",
                        method="delete",
                    )
                    print("*" * 50)
                    if response.status_code != 204:
                        return False
        return True

    # 给某人作品全点赞
    def like_all_work(self, user_id: str):
        works_list = self.client.get_user_works(user_id)
        for item in works_list:
            if not self.client.like_work(work_id=item["id"]):
                return False
        return True


if __name__ == "__main__":
    client = CodeMaoClient()
    print(client.get_user_data(12770114))
