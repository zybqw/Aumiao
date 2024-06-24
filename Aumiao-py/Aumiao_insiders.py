import json
import os
import random
import time
from typing import Any, Dict, List, Optional

# 在获取任何数据时, 链接参数中的`offset`表示忽略前**个作品, `limit`获取之后的作品列表
# offset为非必选项, limit为必选项, 且必须大于等于5, 小于等于200
# 获取某人作品列表limit无限制
# user_id为一串数字, 但api返回时返回类型为字符串, 故在爬虫中采用字符串类型

# 尝试导入requests库
try:
    import requests
    from requests.exceptions import (
        HTTPError,
        ConnectionError,
        Timeout,
        RequestException,
    )
except ModuleNotFoundError:
    # 提示用户未安装requests库,并询问安装位置
    print("检测到您未下载requests库,正在为您安装。")
    step = input(
        "如果安装了多个python版本,请输入要安装的位置（例如:3.x）,否则直接回车跳过: "
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
            HTTPError,
            ConnectionError,
            Timeout,
            RequestException,
        )
    except ModuleNotFoundError:
        # 如果安装失败,则退出程序
        print("安装requests库失败,请手动安装后再运行程序。")
        exit(1)


class CodeMaoData:
    Account: Dict[str, str] = {
        "identity": " ",
        "password": " ",
        "id": " ",
        "nickname": " ",
        "create_time": " ",
        "author_level": " ",
        "description": " ",
    }

    # 预设数据, 用于存储代理、评论内容、表情等
    Pre_Data = {
        "blackroom": ["114514", "1919810", "2233"],
        "comments": [
            "666",
            "加油！:O",
            "针不戳:D",
            "前排:P",
            "沙发*/ω＼*",
            "不错不错",
        ],
        "emojis": [
            "编程猫_666",
            "编程猫_爱心",
            "编程猫_棒",
            "编程猫_爱心",
            "编程猫_抱大腿",
            "编程猫_打call",
            "编程猫_点手机",
            "编程猫_好厉害",
            "编程猫_加油",
            "编程猫_我来啦",
            "魔术喵_魔术",
            "魔术喵_点赞",
            "魔术喵_开心",
            "魔术喵_魔术",
            "魔术喵_点赞",
            "魔术喵_收藏",
            "星能猫_耶",
            "星能猫_好吃",
            "雷电猴_围观",
            "雷电猴_哇塞",
            "雷电猴_哈哈哈",
            "雷电猴_嘻嘻嘻",
        ],
        "answers": [
            "这是{}的自动回复,不知道你在说啥(",
            "{}的自动回复来喽",
            "嗨嗨嗨!这事{}の自动回复鸭!",
            "{}很忙oh,机器人来凑热闹(*＾＾*)",
            "对不起,{}它又搞忘了时间,一定是在忙呢",
            "机器人要开始搅局了,{}说忙完就过来！",
        ],
        "ad": [
            "scp",
            "互赞",
            "赞我",
            "点个",
            "转发",
            "关注",
            "招人",
            "广告",
            "交友",
            "cpdd",
            "处cp",
            "找闺",
            "自动",
            "扫厕所",
            "冲高手",
            "冲大佬",
            "冲传说",
            "戴雨默",
            "光头强",
            "基金会",
            "再创作",
            "找徒弟",
            "协作项目",
            "家族招人",
            "不喜可删",
            "有赞必回",
            "看看我的",
            "粘贴到别人作品",
            "codemao.cn",
        ],
        # ... (其他预设内容, 如评论、表情等)
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
    CONFIG_FILE_PATH: str = os.path.join(os.getcwd(), "config.json")

    def process_reject(self, data, reserve=None, exclude=None):
        """
        Filters keys in a dictionary or list of dictionaries based on reserved or excluded keys.
        Args:
        data: List[Dict] or Dict - the input data to filter.
        reserve: List[str] - keys to include in the output.
        exclude: List[str] - keys to exclude from the output.
        Returns:
        List[Dict] or Dict - the filtered data.
        Raises:
        ValueError - if both reserve and exclude parameters are provided, or if the data type is unsupported.
        """
        if reserve and exclude:
            raise ValueError(
                "请仅提供 'reserve' 或 'exclude' 中的一个参数,不要同时使用。"
            )
        if not isinstance(data, (list, dict)):
            raise ValueError("不支持的数据类型,仅接受列表或字典。")

        def filter_keys(item):
            if reserve is not None:
                return {key: value for key, value in item.items() if key in reserve}
            if exclude is not None:
                return {key: value for key, value in item.items() if key not in exclude}
            return item

        if isinstance(data, list):
            return [filter_keys(item) for item in data]
        return filter_keys(data)


class CodeMaoClient:
    BASE_URL = "https://api.codemao.cn"
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }

    def __init__(self):
        self.session = requests.Session()
        self.cookie_pr = requests.utils.dict_from_cookiejar
        self.session.headers.update(self.HEADERS)
        self.tool = CodeMaoTool()

    def send_request(self, url, method, params=None, data=None, headers=HEADERS):
        url = f"{self.BASE_URL}{url}"
        try:
            response = self.session.request(
                method=method, url=url, headers=headers, params=params, data=data
            )
            response.raise_for_status()
            return response
        except (HTTPError, ConnectionError, Timeout, RequestException) as e:
            print(f"网络请求异常: {e}")
            return None

    # 获取用户账号信息
    # (简略)
    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        response = self.send_request(
            method="get", url=f"/api/user/info/detail/{user_id}"
        )
        if response:
            return self.tool.process_reject(
                data=response.json().get("data").get("userInfo"),
                exclude=["work", "isFollowing"],
            )
        return None

    # (详细)
    def get_user_details(self):
        response = self.send_request(
            method="get",
            url="/web/users/details",
        )

        return self.tool.process_reject(
            data=response.json(),
            reserve=[
                "id",
                "nickname",
                "description",
                "create_time",
                "author_level",
            ],
        )

    def get_user_honor(self, user_id):
        params = {"user_id": user_id}
        response = self.send_request(
            url="/creation-tools/v1/user/center/honor",
            method="get",
            params=params,
        )
        return self.tool.process_reject(
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

    # 获取作品列表的函数
    def get_user_works(self, user_id: str) -> List[int]:
        params = {
            "type": "newest",
            "user_id": user_id,
            "offset": 0,
            "limit": 5,
        }
        response = self.send_request(
            url="/creation-tools/v2/user/center/work-list",
            method="get",
            params=params,
        )

        _dict = []
        for item in range(int(response.json().get("total") / 200) + 1):
            params = {
                "type": "newest",
                "user_id": user_id,
                "offset": item * 200,
                "limit": 200,
            }
            response = self.send_request(
                url="/creation-tools/v2/user/center/work-list",
                method="get",
                params=params,
            )
            _dict.extend(response.json().get("items"))
        result = self.tool.process_reject(data=_dict, reserve=["id", "work_name"])
        return result

    def get_user_fans(self, user_id: str):
        _dict = []
        for item in range(
            int(self.get_user_honor(user_id=user_id)["fans_total"] / 200) + 1
        ):
            params = {
                "user_id": user_id,
                "offset": item * 200,
                "limit": 200,
            }
            response = self.send_request(
                url="/creation-tools/v1/user/fans",
                method="get",
                params=params,
            )
            _dict.extend(json.loads(response.text)["items"])
        result = self.tool.process_reject(data=_dict, reserve=["id", "nickname"])
        return result

    # 登录函数, 处理登录逻辑并保存登录状态
    def login(
        self, method: str, identity=None, password=None, cookies=None
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
            # 重新编写设置cookie的代码,使其更简洁和清晰
            # 获取用户输入的cookie字符串
            try:
                # 将cookie字符串分割成键值对,并存储到cookie_dict字典中
                cookie_dict = dict([item.split("=", 1) for item in cookies.split("; ")])
            except (KeyError, ValueError) as err:
                print("表达式输入不合法 {}".format(err))
                return False
            # 将cookie_dict字典转换为cookiejar对象并设置到ses.cookies中
            self.session.cookies = self.cookie_pr(
                cookie_dict, cookiejar=None, overwrite=True
            )
            response = self.send_request(
                url="/nemo/v2/works/174408420/like",
                method="post",
                data=json.dumps({}),
                # headers={**HEADERS, "cookie": cookie_str},
            )
        if response.status_code == 200:
            return True
        elif response.status_code == 403:
            return "Wrong"
        else:
            print(f"登录失败惹,错误码: {response.status_code}")
            return False


# Example usage
if __name__ == "__main__":
    client = CodeMaoClient()
    if client.login(method="password", identity="Aurzex", password="CODExhr1106.mao"):
        user_details = client.get_user_details()
        print(user_details)
