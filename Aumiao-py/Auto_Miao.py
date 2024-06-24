import json
import os
import random
import time
from typing import Any, Dict, List, Optional

# 导入所需的库和模块
# from bs4 import BeautifulSoup
try:
    from requests import exceptions, session, utils
except ModuleNotFoundError:
    from os import system

    print("检测到您未下载requests库, 正在为您安装")
    step = input("如果安装了多个python版本, 请输入要安装的位置,否则跳过(3.x/N)")
    if step == "N":
        system("pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
    else:
        system(
            f"py -{step} -m pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple"
        )
    from requests import exceptions, session, utils

# 在获取任何数据时, 链接参数中的`offset`表示忽略前**个作品, `limit`获取之后的作品列表
# offset为非必选项, limit为必选项, 且必须大于等于5, 小于等于200
# 获取某人作品列表limit无限制
# user_id为一串数字, 但api返回时返回类型为字符串, 故在爬虫中采用字符串类型


print("欢迎使用Aumiao")
print("bug反馈或新功能建议 e-mail: zybqw@qq.com  QQ:3611198191")
print("仅供学习技术交流, 若对编程猫或您造成损失, 本人概不负责")

CONFIG_FILE_PATH: str = os.path.join(os.getcwd(), "config.json")
HEADERS: Dict[str, str] = {  # 设置请求头
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
}
session = session()

# 初始化账户信息
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


# 发送请求的函数, 根据不同的方法(GET/POST)发送请求
def send_request(url, method, params=None, data=None, headers=HEADERS):
    global session
    try:
        response = session.request(
            method=method, url=url, headers=headers, params=params, data=data
        )
        response.raise_for_status()
        return response
    except exceptions.HTTPError as err:
        print("HTTP错误:", err)
    except exceptions.ConnectionError as err:
        print("连接错误:", err)
    except exceptions.Timeout as err:
        print("超时错误:", err)
    except exceptions.RequestException as err:
        print("其他错误:", err)
    else:
        return response
    time.sleep(20)
    return False


# 从配置文件加载账户信息的函数
def account_load() -> List[Any]:
    try:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        Account.update(data["Account"])
        Data.update(data["Data"])
        return True
    except ValueError as err:
        print("文件错误", err)
        return False


# 为账户信息提供交互式输入的函数
def account_input(method):
    if method == "accounts":
        Account["identity"] = input("输入账号叭    ")
        Account["password"] = input("输入密码叭    ")
    else:
        print("不支持的方法")


# 检查文件
def is_file(path):
    try:
        with open(path, "r"):
            return True
    except IOError:
        return False


# 将文本写入到指定文件的函数
def write(path: str, text: str | Dict, type: str, method="w") -> None:
    with open(path, mode=method, encoding="utf-8") as file:
        if type == "str":
            file.write(text + "\n")
        elif type == "dict":
            file.write(json.dumps(text, ensure_ascii=False, indent=4))
        else:
            print("不支持的写入方法")


# 保留指定key并返回
def process_reject(data, reserve=None, exclude=None):
    if reserve and exclude:
        raise ValueError("请仅提供 'reserve' 或 'exclude' 中的一个参数，不要同时使用。")

    def filter_keys(item):
        if reserve is not None:
            return {key: value for key, value in item.items() if key in reserve}
        elif exclude is not None:
            return {key: value for key, value in item.items() if key not in exclude}
        return item

    if isinstance(data, list):
        return [filter_keys(item) for item in data]
    elif isinstance(data, dict):
        return filter_keys(data)
    else:
        raise ValueError("不支持的数据类型，仅接受列表或字典。")


# 对评论内容进行处理的函数
def process_shielding(content: str) -> str:
    content_bytes = [item.encode("UTF-8") for item in content]
    result = b"\xe2\x80\x8b".join(content_bytes).decode("UTF-8")
    return result


# 时间戳转换为时间
def process_timestamp(time: int) -> str:
    timeArray = time.localtime(time)
    StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return StyleTime


# 获取用户账号信息
def get_user_detials() -> str:
    response = send_request(
        url="https://api.codemao.cn/web/users/details",
        method="get",
    )
    return process_reject(
        data=json.loads(response.text),
        reserve=[
            "id",
            "nickname",
            "description",
            "create_time",
            "author_level",
        ],
    )


# 获取用户信息（简略
def gei_user_data(user_id):
    response = send_request(
        url=f"https://api.codemao.cn/api/user/info/detail/{user_id}",
        method="get",
    )
    return process_reject(
        data=json.loads(response.text)["data"]["userInfo"],
        exclude=["work", "isFollowing"],
    )


# 获取用户荣誉
def get_user_honor(user_id):
    params = {"user_id": user_id}
    response = send_request(
        url="https://api.codemao.cn/creation-tools/v1/user/center/honor",
        method="get",
        params=params,
    )
    return process_reject(
        data=json.loads(response.text),
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


# 获取某人作品列表的函数
def get_user_works(user_id: str) -> List[int]:
    params = {
        "type": "newest",
        "user_id": user_id,
        "offset": 0,
        "limit": 5,
    }
    response = send_request(
        url="https://api.codemao.cn/creation-tools/v2/user/center/work-list",
        method="get",
        params=params,
    )
    _dict = []
    for item in range(int(json.loads(response.text)["total"] / 200) + 1):
        params = {
            "type": "newest",
            "user_id": user_id,
            "offset": item * 200,
            "limit": 200,
        }
        response = send_request(
            url="https://api.codemao.cn/creation-tools/v2/user/center/work-list",
            method="get",
            params=params,
        )
        _dict.extend(json.loads(response.text)["items"])
    result = process_reject(data=_dict, reserve=["id", "work_name"])
    return result


def get_user_fans(user_id: str):
    _dict = []
    for item in range(int(get_user_honor(user_id=user_id)["fans_total"] / 200) + 1):
        params = {
            "user_id": user_id,
            "offset": item * 200,
            "limit": 200,
        }
        response = send_request(
            url="https://api.codemao.cn/creation-tools/v1/user/fans",
            method="get",
            params=params,
        )
        _dict.extend(json.loads(response.text)["items"])
    result = process_reject(data=_dict, reserve=["id", "nickname"])
    print("获取完成")
    return result


# 登录函数, 处理登录逻辑并保存登录状态
def login(method=str) -> Optional[str]:
    # 函数可以在局部修改列表, 字典
    global session
    if method == "password":
        # cookies = utils.dict_from_cookiejar(response.cookies)

        #   soup = BeautifulSoup(
        #       send_request("https://shequ.codemao.cn", "get").text,
        #       "html.parser",
        #   )
        #   见https://api.docs.codemao.work/user/login?id=pid
        #   pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
        pid = "65edCTyg"

        if not is_file(CONFIG_FILE_PATH):
            account_input("accounts")
        response = send_request(
            url="https://api.codemao.cn/tiger/v3/web/accounts/login",
            method="post",
            data=json.dumps(
                {
                    "identity": Account["identity"],
                    "password": Account["password"],
                    "pid": pid,
                }
            ),
        )
    elif method == "cookie":
        # 重新编写设置cookie的代码，使其更简洁和清晰
        # 获取用户输入的cookie字符串
        cookie_str = input("那就输入cookie叭~    ")
        try:
            # 将cookie字符串分割成键值对，并存储到cookie_dict字典中
            cookie_dict = dict([item.split("=", 1) for item in cookie_str.split("; ")])
            # 构造新的cookie字符串
            cookie_str = (
                "acw_tc="
                + cookie_dict["acw_tc"]
                + "; authorization="
                + cookie_dict["authorization"]
            )
        except (KeyError, ValueError) as err:
            print("表达式输入不合法 {}".format(err))
            return False
        # 将cookie_dict字典转换为cookiejar对象并设置到ses.cookies中
        session.cookies = utils.cookiejar_from_dict(
            cookie_dict, cookiejar=None, overwrite=True
        )
        response = send_request(
            url="https://api.codemao.cn/nemo/v2/works/174408420/like",
            method="post",
            data=json.dumps({}),
            # headers={**HEADERS, "cookie": cookie_str},
        )
    if response.status_code == 200:
        print("登录成功惹")
        return True
    elif response.status_code == 403:
        if method == "password":
            print("账号或密码错误了捏")
            if is_file(CONFIG_FILE_PATH):
                print("您好像更改过配置文件或账户密码, 请重新输入捏")
                Account["identity"] = input("输入账号叭    ")
                Account["password"] = input("输入密码叭    ")
            return False
        if method == "cookie":
            print("测试失败！，请重新输入")
    else:
        print(f"登录失败惹,错误码: {response.status_code}")
        return False


# 获取随机昵称
def get_name_random():
    response = send_request(
        method="get",
        url="https://api.codemao.cn/api/user/random/nickname",
    )
    return json.loads(response.text)["data"]["nickname"]


# 获取新作品的函数
def get_works_new(limit: int) -> List[Dict[str, str | int]]:
    params = {"limit": limit}
    response = send_request(
        url="https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work",
        method="get",
        params=params,
    )  # 为防止封号,limit建议调大
    _dict = json.loads(response.text)
    print("\n已找到{}个新作品捏".format(len(_dict["items"])))
    return process_reject(
        data=_dict["items"],
        reserve=[
            "work_id",
            "work_name",
            "user_id",
            "nickname",
            "views_count",
            "likes_count",
        ],
    )
    # return [{key: value for key, value in item.items() if key not in ["preview_url", "avatar_url"]} for item in _dict["items"]]


# 获取评论区特定信息
def get_comments_detail(
    work_id: int,
    method: str,
) -> List[str] | List[Dict[str, int | bool]]:
    result = []
    try:
        params = {"limit": 20, "offset": 0}
        response = send_request(
            url=f"http://api.codemao.cn/creation-tools/v1/works/{work_id}/comments",
            method="get",
            params=params,
        )
        num = json.loads(response.text)["page_total"]
    except (KeyError, NameError) as err:
        print(err)
        return False
    for item in range(
        int(num / 20) + 1
    ):  # 等效于num // 20 , floor(num / 20) ,int(num / 20)
        try:
            params = {"limit": 20, "offset": item * 20}
            response = send_request(
                url=f"http://api.codemao.cn/creation-tools/v1/works/{work_id}/comments",
                method="get",
                params=params,
            )  # limit 根据评论+回复综合来定
            comments = json.loads(response.text)["items"]
            if method == "user_id":
                result = [item["user"]["id"] for item in comments]
            elif method == "comments":
                result.extend(
                    process_reject(
                        data=comments,
                        reserve=["id", "content", "is_top"],
                    )
                )
            else:
                print("不支持的请求方法")
        except (KeyError, NameError) as err:
            print(err)
            pass
        return result
    return False


# 获取工作室简介(简易)
def get_shops_simple():
    # 需登录工作室成员账号
    response = send_request(
        url="https://api.codemao.cn/web/work_shops/simple", method="get"
    )
    result = json.loads(response.text)["work_shop"]
    return result


# 获取工作室简介
def get_shop_detials(id):
    response = send_request(url=f"https://api.codemao.cn/web/shops/{id}", method="get")
    result = process_reject(
        data=json.loads(response.text),
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
def update_shop_detials(description, id, name, preview_url):
    response = send_request(
        url="https://api.codemao.cn/web/work_shops/update",
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
    if response.status_code == 200:
        print("\n更新成功")
    else:
        print("\n更新失败,状态码 {}".format(response.status_code))


# 清除作品广告的函数
def clear_ad() -> bool:
    works_list = get_user_works(Account["id"])
    for item0 in works_list:
        comments = get_comments_detail(work_id=item0["id"], method="comments")
        work_id = item0["id"]
        for item1 in comments:
            comment_id = item1["id"]
            connect = item1["content"].lower()  # 转换小写
            if (
                any(item2 in connect for item2 in Data["ad"])
                and not item1["is_top"]  # 取消置顶评论监测
            ):
                print("在作品 {} 中发现广告: {} ".format(item0["work_name"], connect))
                response = send_request(
                    url=f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment/{comment_id}",
                    method="delete",
                )
                print("*" * 50)
                if response.status_code == 204:
                    print("清除成功")
                else:
                    print("清除失败,状态码 {}".format(response.status_code))
    print("清除完毕")


# 清除旧数据的函数
def clear_redpoint() -> None:
    item = 0
    while True:
        record = send_request(
            url="https://api.codemao.cn/web/message-record/count",
            method="get",
        )
        if len(set([json.loads(record.text)[i]["count"] for i in range(3)]) | {0}) == 1:
            break
        # 精简代码
        params = {
            "query_type": "ANYTHING",
            "limit": 200,
            "offset": item,
        }
        query_types = ["LIKE_FORK", "COMMENT_REPLY", "SYSTEM"]
        responses = {}
        for query_type in query_types:
            params["query_type"] = query_type
            responses[query_type] = send_request(
                url="https://api.codemao.cn/web/message-record",
                method="get",
                params=params,
            ).status_code

            item += 200
        if len(set(responses.values()) | {200}) != 1:
            print("\n消息清除失败惹,错误代码: ")
            print("点赞消息状态码: {}".format(responses["LIKE_FORK"]))
            print("评论回复消息状态码: {}".format(responses["COMMENT_REPLY"]))
            print("系统消息状态码: {}".format(responses["SYSTEM"]))
    print("\n信箱已设置全部已读惹")


# 给某人作品全点赞
def like_all_work(user_id: str):
    works_list = get_user_works(user_id)
    for item in works_list:
        response = send_request(
            url="https://api.codemao.cn/nemo/v2/works/{}/like".format(item["id"]),
            method="post",
            data=json.dumps({}),
        )
        if response.status_code == 200:
            print("点赞成功    " + str(item["work_name"]))
        else:
            print(f"点赞失败,错误代码:{response.status_code}")


# 关注的函数
def follow_work(user_id: int) -> bool:
    response = send_request(
        url=f"https://api.codemao.cn/nemo/v2/user/{user_id}/follow",
        method="post",
        data=json.dumps({}),
    )
    if response.status_code == 204:
        print("关注成功")
    else:
        print(f"关注失败,错误代码:{response.status_code}")


# 收藏的函数
def collection_work(work_id: int) -> bool:
    response = send_request(
        url=f"https://api.codemao.cn/nemo/v2/works/{work_id}/collection",
        method="post",
        data=json.dumps({}),
    )
    if response.status_code == 200:
        print("收藏成功")
    else:
        print(f"收藏失败,错误代码:{response.status_code}")


# 对某个作品进行点赞的函数
def like_work(work_id: int) -> bool:
    # 对某个作品进行点赞
    response = send_request(
        url=f"https://api.codemao.cn/nemo/v2/works/{work_id}/like",
        method="post",
        data=json.dumps({}),
    )
    if response.status_code == 200:
        print("点赞成功")
    else:
        print(f"点赞失败,错误代码:{response.status_code}")


# 对某个作品进行评论的函数
def comment_work(work_id: int) -> bool:
    """对某个作品进行评论"""
    comment = process_shielding(random.choice(Data["comments"]))
    emoji = ",".join(random.sample(Data["emojis"], random.randint(1, 3)))
    response = send_request(
        url=f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment",
        method="post",
        data=json.dumps(
            {
                "content": comment,
                "emoji_content": emoji,
            }
        ),
    )
    if response.status_code == 201:
        print(
            "\n".join(
                [
                    "评论成功",
                    f"评论内容  {comment}",
                    f"附带表情  {emoji}",
                ]
            )
        )
    else:
        print(f"评论发送失败,错误代码:{response.status_code}\n")


# 获取新回复的函数
def get_new_replies() -> List[Dict[str, Any]]:
    _dict = []
    while True:
        record = send_request(
            url="https://api.codemao.cn/web/message-record/count",
            method="get",
        )
        reply_num = json.loads(record.text)[0]["count"]
        list_num = 200 if reply_num > 200 else reply_num
        if reply_num == 0:
            break
        if reply_num > 200:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": 200,
            }
            reply_num -= 200
        if reply_num > 5:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": reply_num,
            }
        else:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": 5,
            }

        response = send_request(
            url="https://api.codemao.cn/web/message-record",
            method="get",
            params=params,
        )
        _dict.extend(json.loads(response.text)["items"][0:list_num])
    return _dict


# 回复新回复的函数
def reply_work(replies: List[Dict[str, Any]]) -> None:
    for reply in replies:
        answer = random.choice(Data["answers"])
        print("回复类型  {}".format(reply["type"]))
        if reply["type"] == "WORK_COMMENT":
            response = send_request(
                url="https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                    json.loads(reply["content"])["message"]["business_id"],
                    json.loads(reply["content"])["message"]["comment_id"],
                ),
                method="post",
                data=json.dumps(
                    {
                        # "parent_id": first_reply["reply_id"],A
                        "parent_id": 0,
                        "content": answer,
                    }
                ),
            )

        elif reply["type"] in [
            "WORK_REPLY",
            "WORK_REPLY_REPLY",
        ]:
            response = send_request(
                url="https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                    json.loads(reply["content"])["message"]["business_id"],
                    json.loads(reply["content"])["message"]["replied_id"],
                ),
                method="post",
                data=json.dumps(
                    {
                        "parent_id": reply["reference_id"],
                        "content": answer,
                    }
                ),
            )
        else:
            print(f"不支持的回复类型{reply['type']}")
            continue
        if response.status_code == 201:
            print(
                "\n".join(
                    [
                        "回复成功",
                        "回复作品  {} {}".format(
                            json.loads(reply["content"])["message"]["business_name"],
                            json.loads(reply["content"])["message"]["business_id"],
                        ),
                        "回复对象  {} {}".format(
                            json.loads(reply["content"])["sender"]["nickname"],
                            reply["sender_id"],
                        ),
                        "回复内容  {}".format(
                            json.loads(reply["content"])["message"]["reply"]
                            # json.loads(reply["content"])["message"]["COMMENT"]
                        ),
                        f"发送内容  {answer}\n",
                    ]
                )
            )
        else:
            print(f"回复发送失败,错误代码:{response.status_code}\n")


# 主函数, 程序的入口点
def main() -> None:
    work_num = 0
    like_log = []
    if is_file(CONFIG_FILE_PATH):
        account_load()
    # cookie_or_account = input("\n是想账号登录(A)还是cookie(C)捏？    ")
    cookie_or_account = "A"
    while True:
        if cookie_or_account == "A":
            if login(method="password"):
                break
        elif cookie_or_account == "C":
            if login(method="cookie"):
                break
        else:
            print("小笨蛋,输入错误惹,快看看是不是输入的A或者C")
            cookie_or_account = input("\n是想账号登录(A)还是cookie(C)捏？    ")
    Account.update(get_user_detials())
    print("HI! {} 欢迎使用Aumiao".format(Account["nickname"]))
    if not is_file(CONFIG_FILE_PATH):
        Data.update(Pre_Data)
        Data["answers"] = [text.format(Account["nickname"]) for text in Data["answers"]]
    write(
        path=CONFIG_FILE_PATH,
        text={"Account": Account, "Data": Data},
        type="dict",
    )
    print("祝您使用愉快")
    while True:
        print("来选择工作方式捏")
        print("点赞(A)&评论(B)&收藏(C)&关注(D)&回复(E)")
        print("信箱全部已读(F)&清除作品广告(G)&点赞作者所有作品(H)&工作室常驻置顶(I)")
        print("获取粉丝列表(J)获取随机昵称(K)&查看账号创建时间(L)")
        # steps = input("tips:可多选    ")
        steps = "A"
        if any(
            step in steps
            for step in [chr(item) for item in range(ord("A"), ord("L") + 1)]
        ):
            break
        else:
            print("输入错误惹")
    if "J" in steps:
        fans_list = get_user_fans(Account["id"])
        fans_list.reverse()
        with open(
            os.path.join(os.getcwd(), "fans_list.txt"), mode="w", encoding="utf-8"
        ) as f:
            for item in fans_list:
                f.write("昵称:  {}\n".format(item["nickname"]))
                f.write("编号:  {}\n".format(item["id"]))
                f.write("*" * 50 + "\n")

    if "K" in steps:
        print("\n")
        for i in range(0, 5):
            print(get_name_random())
    if "L" in steps:
        print("\n创建时间为", process_timestamp(Account["create_time"]))
    if not any(
        step in steps for step in [chr(item) for item in range(ord("A"), ord("I") + 1)]
    ):
        print("\n执行完毕")
    while True:
        if any(step in steps for step in ["A", "B", "C", "D", "H"]):
            work_list = get_works_new(limit=200)  # 为防止封号,limit建议调大
            for item in work_list:
                work_num += 1
                print("*" * 50)
                print("已经访问了{}个作品".format(work_num))
                print("作品名称 {}".format(item["work_name"]))
                print("作品编号 {}".format(item["work_id"]))
                print("作者昵称 {}".format(item["nickname"]))
                print("作者编号 {}\n".format(item["user_id"]))
                if "A" in steps:
                    if not item["work_id"] in like_log:
                        like_work(item["work_id"])
                        time.sleep(random.randint(10, 20))
                        like_log.append(item["work_id"])
                    else:
                        print("已经点赞过了哟~")
                        time.sleep(random.randint(30, 40))
                if "H" in steps:
                    like_all_work(item["user_id"])
                if "C" in steps:
                    collection_work(item["work_id"])
                if "D" in steps:
                    follow_work(item["user_id"])
                if "B" in steps:
                    if Account["id"] in get_comments_detail(
                        item["work_id"], method="user_id"
                    ):
                        print("找到一个已经发送过的(～￣▽￣)～")
                        time.sleep(30)
                        continue
                    if (
                        item["views_count"] <= 1500
                        and item["likes_count"] <= 50
                        and item["user_id"] not in Data["blackroom"]
                    ):
                        comment_work(item["work_id"])
                        time.sleep(random.randint(60, 100))
                    else:
                        print("这个作品不适于发送qwq")
        if "E" in steps:
            replies_list = get_new_replies()
            print(replies_list)
            reply_work(replies_list)
            time.sleep(random.randint(5, 10))
        if "F" in steps:
            clear_redpoint()
            time.sleep(100)
        if "G" in steps:
            clear_ad()
            time.sleep(100)
        if "I" in steps:
            detials = get_shops_simple()
            description = get_shop_detials(detials["work_subject_id"])["description"]
            update_shop_detials(
                description=description,
                id=detials["id"],
                name=detials["name"],
                preview_url=detials["preview_url"],
            )
            time.sleep(200)


# 程序入口, 如果文件是直接运行, 则执行main函数
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as err:
            print(err)
            time.sleep(400)
