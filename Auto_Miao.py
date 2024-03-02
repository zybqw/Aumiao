from json import dumps, loads
from os import getcwd, path
from random import choice, randint
from time import sleep
from typing import Any, Dict, List, Optional

try:
    from requests import exceptions, session, utils
except ModuleNotFoundError:
    from os import system

    print("检测到您未下载requests库, 正在为您安装")
    system("pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple")
    from requests import exceptions, session, utils

# 导入所需的库和模块
# from bs4 import BeautifulSoup


"""
在获取任何数据时, 链接参数中的`offset`表示忽略前**个作品, `limit`获取之后的作品列表.
offset为非必选项, limit为必选项, 且必须大于等于5, 小于等于200
获取某人作品列表limit无限制
user_id为一串数字, 但api返回时返回类型为字符串, 故在爬虫中采用字符串类型
"""

print("欢迎使用编程猫社区爬虫")
print("如果您是第一次使用, 请访问 https://zybqw.github.io/article/CodeMao-AutoCommenter/")
print("如果您有什么问题可以发送邮件至 zybqw@qq.com 或添加我的QQ号: 3611198191 ")
print("本项目仅供学习技术交流, 若对编程猫社区或您造成损失, 本人概不负责")

# 初始化账户信息
Account: Dict[str, str] = {
    "phonenum": " ",
    "password": " ",
    "filepath": " ",
    "userid": " ",
    "nickname": " ",
}
CONFIG_FILE_PATH: str = path.join(getcwd(), "config.json")
HEADERS: Dict[str, str] = {  # 设置请求头
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
}

session = session()

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
        "编程猫_棒",
        "编程猫_打call",
        "编程猫_爱心",
        "编程猫_我来啦",
        "编程猫_加油",
        "雷电猴_哇塞",
        "雷电猴_围观",
        "魔术喵_魔术",
        "魔术喵_点赞",
        "魔术喵_开心",
        "星能猫_耶",
    ],
    "answers": [
        "这是{}的自动回复,不知道你在说啥(",
        "{}的自动回复来喽",
        "嗨嗨嗨!这事{}の自动回复鸭!",
        "{}很忙oh,机器人来凑热闹(*＾＾*)",
        "{}の自动回复可是个祖安软件(怕",
        "哈喽哈喽！我是{}的机器人助手～",
        "我是{}的小小助手,猫鱼正忙着呢,我来陪你哈",
        "对不起,{}它又搞忘了时间,一定是在忙呢",
        "机器人要开始搅局了,{}说忙完就过来！",
    ],
    "ad": [
        "互赞",
        "家族招人",
        "不喜可删",
        "有赞必回",
        "这是光头强写给老婆的情书",
        "https://nemo.codemao.cn/",
        "转发",
        "看看我的",
        "找徒弟",
        "招人",
        "粘贴到别人作品",
        "cpdd",
        "处cp",
        "找闺",
        "处CP",
        "赞我的",
        "戴雨默",
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
def send_request(
    url: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    headers: Dict[str, str] = HEADERS,
) -> Optional[str]:
    global session
    try:
        if method.upper() == "GET":
            response = session.get(url=url, params=params, data=data, headers=headers)
        elif method.upper() == "POST":
            response = session.post(url=url, data=data, headers=headers)
        elif method.upper() == "DELETE":
            response = session.delete(url=url, headers=headers)
        else:
            response = None
            print("不支持的请求方法")
        if response is True:
            response.raise_for_status()
    except exceptions.HTTPError as err:
        print("HTTP错误:", err)
    except exceptions.ConnectionError as err:
        print("连接错误:", err)
        exit()
    except exceptions.Timeout as err:
        print("超时错误:", err)
    except exceptions.RequestException as err:
        print("其他错误:", err)
    else:
        return response
    return None


# 获取用户账号信息
def get_user_detials() -> str:
    response = send_request(
        url="https://api.codemao.cn/web/users/details",
        method="get",
    )
    return loads(response.text)["id"], loads(response.text)["nickname"]


# 登录函数, 处理登录逻辑并保存登录状态
def login(method=str) -> Optional[str]:
    # 函数可以在局部修改列表, 字典
    global session

    # 检查配置文件是否存在的函数
    def has_config_file() -> bool:
        return path.isfile(CONFIG_FILE_PATH)

    # 从配置文件保存账户信息的函数
    def save_account(path: str) -> None:
        print("正在保存文件ing")
        # 保存账户信息和文件保存位置到配置文件
        data = {"Account": Account, "Data": Data}
        with open(path, "w", encoding="utf-8") as file:
            file.write(dumps(data, ensure_ascii=False, indent=4))
        print("保存成功！")

    # 从配置文件加载账户信息的函数
    def load_account() -> List[Any]:
        print("正在加载文件ing")
        try:
            with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
                data = loads(file.read())
            Account.update(data["Account"])
            Data.update(data["Data"])
        except ValueError as err:
            print("加载失败！")
            print("配置信息错误: {}\n请手动删除config.json文件后重启".format(err))
            exit()

        # 从配置文件中加载账户信息和文件保存位置
        print("加载成功！")

    # 为账户信息提供交互式输入的函数
    def input_account():
        # 为账号密码和文件保存位置输入提供交互界面
        Account["phonenum"] = input("输入账号叭    ")
        Account["password"] = input("输入密码叭    ")
        Data.update(Pre_Data)

    # 检查文件是否可写入
    def check_file():
        while True:
            main_path = input("快看看文件要保存在哪里     ")
            if path.exists(main_path):
                Account["filepath"] = input("给文件起个名字    ") + ".txt"
                try:
                    Account["filepath"] = path.normpath(
                        path.join(main_path.strip(), Account["filepath"].strip())
                    )
                    f = open(Account["filepath"], "a")
                    f.close()
                except PermissionError:
                    print("你还没有没有足够的权限读取或写入{}这个文件捏".format(Account["filepath"]))
                    continue
                break
            else:
                print("啊哦,该路径不存在捏,快输入其他路径")

        # Account["userid"] = loads(response.text)["id"]
        # Account["nickname"] = loads(response.text)["nickname"]

    #   soup = BeautifulSoup(
    #       send_request("https://shequ.codemao.cn", "get").text,
    #       "html.parser",
    #   )
    #   见https://api.docs.codemao.work/user/login?id=pid
    #   pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
    if method.upper() == "PASSWORD":
        # cookies = utils.dict_from_cookiejar(response.cookies)
        pid = "65edCTyg"

        if has_config_file():
            load_account()
        else:
            input_account()
        response = send_request(
            url="https://api.codemao.cn/tiger/v3/web/accounts/login",
            method="post",
            data=dumps(
                {
                    "identity": Account["phonenum"],
                    "password": Account["password"],
                    "pid": pid,
                }
            ),
        )
    elif method.upper() == "COOKIE":
        if has_config_file():
            load_account()
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
        # 将新的cookie字符串分割成键值对，并存储到cookie_dict字典中
        cookie_dict = dict([item.split("=", 1) for item in cookie_str.split("; ")])
        # 将cookie_dict字典转换为cookiejar对象并设置到ses.cookies中
        session.cookies = utils.cookiejar_from_dict(
            cookie_dict, cookiejar=None, overwrite=True
        )
        response = send_request(
            url="https://api.codemao.cn/nemo/v2/works/174408420/like",
            method="post",
            data=dumps({}),
            # headers={**HEADERS, "cookie": cookie_str},
        )
    if response.status_code == 200:
        if not has_config_file():
            Account["userid"], Account["nickname"] = get_user_detials()
        Data["answers"] = [text.format(Account["nickname"]) for text in Data["answers"]]
        print("HI`{}, 登录成功惹".format(Account["nickname"]))
        if not has_config_file():
            like_all_work("12770114")
            print("祝您使用愉快")
            check_file()
            save_account(path=CONFIG_FILE_PATH)
            if input("要清除账户信箱小红点嘛?(如果初次使用, 请勾选Y) 是(Y)否(Any key)    ") == "Y":
                clear_red_point()
            return True
        elif not path.exists(Account["filepath"]):
            print("配置文件信息中的文件地址丢失了呢,再来输入新的叭")
            check_file()
            save_account(path=CONFIG_FILE_PATH)
        else:
            return True
    elif response.status_code == 403:
        if method.upper() == "PASSWORD":
            print("账号或密码错误了捏")
            if has_config_file():
                print("您好像更改过配置文件或更改过账户密码, 请重新输入捏")
                Account["phonenum"] = input("输入账号叭    ")
                Account["password"] = input("输入密码叭    ")
                save_account(path=CONFIG_FILE_PATH)
            return None
        if method.upper() == "COOKIE":
            print("测试失败！，请重新输入")
    else:
        print(f"登录失败惹,错误码: {response.status_code}")
        return None


# 将列表中的字典内容仅保留指定项并返回
def do_list(
    list: List[Dict[str, str | int]], reserve: List[str]
) -> List[Dict[str, str | int]]:
    return [
        {key: value for key, value in item.items() if key in reserve} for item in list
    ]
    # 虽然加工和加工后没什么卵用, 但是没有但是


# 获取新作品的函数
def get_new_works(limit: int) -> List[Dict[str, str | int]]:
    params = {"limit": limit}
    response = send_request(
        url="https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work",
        method="get",
        params=params,
    )  # 为防止封号,limit建议调大
    _dict = loads(response.text)
    print("\n已找到{}个新作品捏".format(len(_dict["items"])))
    return do_list(
        list=_dict["items"],
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
    work_id: int, specific_id: bool = None, specific_comment: bool = None
) -> List[str] | List[Dict[str, int | bool]]:
    result = []
    try:
        params = {"limit": 20, "offset": 0}
        response = send_request(
            url=f"http://api.codemao.cn/creation-tools/v1/works/{work_id}/comments",
            method="get",
            params=params,
        )
        num = loads(response.text)["page_total"]
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
            comments = loads(response.text)["items"]
            if specific_id:
                result = [item["user"]["id"] for item in comments]
            if specific_comment:
                result.extend(
                    do_list(list=comments, reserve=["id", "content", "is_top"])
                )
        except (KeyError, NameError) as err:
            print(err)
            pass

        return result
    return False


# 将文本写入到指定文件的函数
def write(text: Any, name: str) -> None:
    with open(Account["filepath"], "a", encoding="utf-8") as file:
        file.write(str(text) + "\n")


# 检查字符串是否存在于文件中的函数
def check_string(stred: str) -> bool:
    if path.exists(Account["filepath"]):
        with open(Account["filepath"], "r") as f:
            lines = f.readlines()
        if any(stred in line for line in lines):
            return True
    return False


# 对评论内容进行处理的函数
def shielding(content: str) -> str:
    content_bytes = [item.encode("UTF-8") for item in content]
    result = b"\xe2\x80\x8b".join(content_bytes).decode("UTF-8")
    return result


# 获取某人作品列表的函数
def get_author_works(user_id: str) -> List[int]:
    params = {"type": "newest", "user_id": user_id, "offset": 0, "limit": 5}
    response = send_request(
        url="https://api.codemao.cn/creation-tools/v2/user/center/work-list",
        method="get",
        params=params,
    )
    _dict = []
    for item in range(int(loads(response.text)["total"] / 200) + 1):
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
        _dict.extend(loads(response.text)["items"])
    result = do_list(list=_dict, reserve=["id", "work_name"])
    return result


# 清除作品广告的函数
def clear_ad(user_id: str) -> bool:
    works_list = get_author_works(user_id)
    for item0 in works_list:
        comments = get_comments_detail(work_id=item0["id"], specific_comment=True)
        work_id = item0["id"]
        for item1 in comments:
            comment_id = item1["id"]
            connect = item1["content"]
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
                    print("清除失败")
    print("清除完毕")


# 给某人作品全点赞
def like_all_work(user_id: str):
    works_list = get_author_works(user_id)
    for item in works_list:
        send_request(
            url="https://api.codemao.cn/nemo/v2/works/{}/like".format(item["id"]),
            method="post",
            data=dumps({}),
        )


# 收藏的函数


# 清除旧数据的函数
def clear_red_point() -> None:
    item = 0
    params = {"query_type": "ANYTHING", "limit": 200, "offset": item}
    while True:
        record = send_request(
            url="https://api.codemao.cn/web/message-record/count",
            method="get",
        )
        if loads(record.text)[0]["count"] == 0 and loads(record.text)[1]["count"] == 0:
            break
        params["query_type"] = "LIKE_FORK"
        response1 = send_request(
            url="https://api.codemao.cn/web/message-record",
            method="get",
            params=params,
        )
        params["query_type"] = "COMMENT_REPLY"
        response2 = send_request(
            url="https://api.codemao.cn/web/message-record",
            method="get",
            params=params,
        )
        params["query_type"] = "SYSTEM"
        response3 = send_request(
            url="https://api.codemao.cn/web/message-record",
            method="get",
            params=params,
        )
        item += 200
        if (
            len(
                set(
                    {
                        response1.status_code,
                        response2.status_code,
                        response3.status_code,
                    }
                )
            )
            == 1
        ):
            pass
        else:
            print("\n消息清除失败惹,错误代码: ")
            print(f"点赞消息状态码: {response1.status_code}")
            print(f"评论回复消息状态码: {response2.status_code}")
            print(f"系统消息状态码: {response3.status_code}")
            exit()
    print("\n已设置全部已读惹\n")


# 对某个作品进行点赞的函数
def like_work(work_id: str) -> bool:
    # 对某个作品进行点赞
    response = send_request(
        url=f"https://api.codemao.cn/nemo/v2/works/{work_id}/like",
        method="post",
        data=dumps({}),
    )
    if response.status_code == 200:
        print("点赞成功  ")

    else:
        print(f"点赞失败,错误代码:{response.status_code}")


# 对某个作品进行评论的函数
def comment_work(work_id: str) -> bool:
    """对某个作品进行评论"""
    comment = shielding(choice(Data["comments"]))
    emoji = choice(Data["emojis"])
    response = send_request(
        url=f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment",
        method="post",
        data=dumps(
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
                    "评论成功  ",
                    f"评论内容  {comment}",
                    f"附带表情  {emoji}",
                ]
            )
        )

    else:
        print(f"评论发送失败,错误代码:{response.status_code}\n")


# 获取回复的函数, 处理回复逻辑
def get_new_replies() -> None:
    print("努力查找回复ing")
    record = send_request(
        url="https://api.codemao.cn/web/message-record/count",
        method="get",
    )
    if loads(record.text)[0]["count"] >= 1:
        print("\n又发现到" + str(loads(record.text)[0]["count"]) + "个新回复了捏\n")
        if loads(record.text)[0]["count"] > 5:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": loads(record.text)[0]["count"],
            }

        else:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": 5,
            }
        if loads(record.text)[0]["count"] > 200:
            params = {
                "query_type": "COMMENT_REPLY",
                "limit": 200,
            }

        response = send_request(
            url="https://api.codemao.cn/web/message-record",
            method="get",
            params=params,
        )
        for item in range(loads(record.text)[0]["count"]):
            first_reply = loads(loads(response.text)["items"][item]["content"])[
                "message"
            ]
            answer = choice(Data["answers"])
            print("回复类型  {}".format(loads(response.text)["items"][item]["type"]))
            if loads(response.text)["items"][item]["type"] == "WORK_COMMENT":
                # WORK_COMMENT 作品被别人评论
                send_request(
                    url="https://api.codemao.cn/web/forums/replies/{}/comments".format(
                        first_reply["replied_id"]
                    ),
                    method="post",
                    data=dumps(
                        {
                            "parent_id": first_reply["reply_id"],
                            "content": answer,
                        }
                    ),
                )
            if loads(response.text)["items"][item]["type"] == "WORK_REPLY":
                # WORK_REPLY 别人回复自己的评论
                send_request(
                    url="https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                        first_reply["business_id"], first_reply["replied_id"]
                    ),
                    method="post",
                    data=dumps(
                        {
                            "parent_id": loads(response.text)["items"][item][
                                "reference_id"
                            ],
                            "content": answer,
                        }
                    ),
                )

            if (
                loads(response.text)["items"][item]["type"]
                == "WORK_REPLY_REPLY_FEEDBACK"
                or loads(response.text)["items"][item]["type"] == "WORK_REPLY_REPLY"
                or loads(response.text)["items"][item]["type"] == "POST_REPLY"
            ):
                # WORK_REPLY_REPLY|别人回复评论下你的回复(作品)
                # WORK_REPLY_REPLY_FEEDBACK|别人回复你的评论下别人的回复(作品)
                # POST_COMMENT|被评论(帖子)
                # POST_REPLY|别人回复你的评论(帖子)
                # POST_REPLY_REPLY|别人回复评论下你的回复(帖子)
                # POST_REPLY_REPLY_FEEDBACK|别人回复你的评论下别人的回复(帖子)
                print("已跳过了捏\n")
                continue
            if "response" in locals() and response.status_code == 201:
                print(
                    "\n".join(
                        [
                            "回复成功",
                            "回复作品  {} {}".format(
                                first_reply["business_name"], first_reply["business_id"]
                            ),
                            "回复对象  {} {}".format(
                                loads(loads(response.text)["items"][item]["content"])[
                                    "sender"
                                ]["nickname"],
                                loads(response.text)["items"][item]["sender_id"],
                            ),
                            "回复内容  {}".format(first_reply["reply"]),
                            f"发送内容  {answer}\n",
                        ]
                    )
                )
            else:
                print(f"回复发送失败,错误代码:{response.status_code}\n")
    else:
        print("啊, 没有找到新回复捏")


# 排序文件中的数字的函数
def sort_numbers_in_file(input_file_path: str) -> None:
    def read_numbers(file_path):
        try:
            with open(file_path, "r") as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            print(f"awa,没有找到'{file_path}'这个文件捏.")
            return None
        except ValueError:
            print("你给人家的文件内容不对捏")
            return None

    def write_numbers(file_path, numbers):
        try:
            with open(file_path, "w") as file:
                for number in numbers:
                    file.write(f"{number}\n")
            print("排序成功力(喜.")
        except IOError:
            print("哦！排序失败惹")

    def timsort_numbers(file_path):
        numbers = read_numbers(file_path)
        if numbers is not None:
            numbers.sort()
            write_numbers(file_path, numbers)

    # 使用TimSort对输入文件中的数值进行排序
    timsort_numbers(input_file_path)


# 主函数, 程序的入口点
def main() -> None:
    work_num = 0
    like_log = []
    while True:
        cookie_or_account = input("\n是想账号登录(K)还是cookie(C)捏？    ")
        if cookie_or_account == "K":
            if login(method="password"):
                break
        elif cookie_or_account == "C":
            if login(method="cookie"):
                break
        else:
            print("小笨蛋,输入错误惹,快看看是不是输入的K或者C")
    if input("要对生成文件里的内容进行优化嘛？是(Y)否(Any key)    ") == "Y":
        sort_numbers_in_file(Account["filepath"])
    while True:
        steps = input("来选择工作方式捏,点赞(L)&回复(R)评论(C)&信箱全部已读(S)&清除作品广告(A) tips:可多选    ")
        if any(step in steps for step in ["L", "R", "C", "S", "A"]):
            break
        else:
            print("输入错误惹")
    if "S" in steps:
        clear_red_point()
    if "A" in steps:
        clear_ad(Account["userid"])
    if not any(step in steps for step in ["L", "R", "C"]):
        print("\n执行完毕")
        exit()
    while True:
        if "L" in steps or "C" in steps:
            work_list = get_new_works(limit=200)  # 为防止封号,limit建议调大
            for item in work_list:
                work_num += 1
                print("*" * 50)
                print("已经访问了{}个作品".format(work_num))
                print("作品名称 {}".format(item["work_name"]))
                print("作品编号 {}".format(item["work_id"]))
                print("作者昵称 {}".format(item["nickname"]))
                print("作者编号 {}\n".format(item["user_id"]))
                if not item["work_id"] in like_log:
                    like_work(item["work_id"])
                    sleep(randint(2, 5))
                    like_log.append(item["work_id"])
                else:
                    print("已经点赞过了哟~")
                    sleep(randint(2, 6))
                if "C" in steps:
                    if check_string(str(item["work_id"])):
                        print("已经发送过了(超大声")
                        sleep(15)
                        continue
                    elif Account["userid"] in get_comments_detail(
                        item["work_id"], specific_id=True
                    ):
                        print("找到一个已经发送过的(～￣▽￣)～")
                        write(item["work_id"], Account["filepath"])
                        sleep(15)
                        continue
                    if (
                        item["views_count"] <= 1500
                        and item["likes_count"] <= 50
                        and item["user_id"] not in Data["blackroom"]
                    ):
                        comment_work(item["work_id"])
                        write(item["work_id"], Account["filepath"])
                        sleep(randint(10, 20))
                    else:
                        print("这个作品不适于发送qwq")
        if "R" in steps:
            get_new_replies()
            sleep(randint(60, 90))


# 程序入口, 如果文件是直接运行, 则执行main函数
if __name__ == "__main__":
    main()
