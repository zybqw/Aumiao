from os import getcwd, path, remove, access, W_OK, R_OK
from requests import Session, utils, post, get
from random import choice, randint
from json import dumps, loads
from bs4 import BeautifulSoup
from configparser import ConfigParser
from time import sleep
from requests.exceptions import RequestException

CONFIG_FILE_PATH = path.join(getcwd(), "config.ini")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
}
UNDO_LIST = ["18996184"]
FILE_NAME = "qwq.txt"
USERDICT = {}

session = Session()


def send_request(url, method, data, headers):
    global response
    try:
        if method.upper() == "GET":
            response = get(url, params=data, headers=headers)
        elif method.upper() == "POST":
            response = post(url, data=data, headers=headers)
        else:
            print(f"不支持的请求方法: {method}")
            return None
        response.raise_for_status()  # 如果响应状态码不是200，就主动抛出异常
    except RequestException as e:
        print(f"网络请求出错: {e}")
        return None
    else:
        return response


def has_config_file():
    """检查是否已存在配置文件"""
    return path.isfile(CONFIG_FILE_PATH)


def save_account(information, path):
    """保存账户信息和文件保存位置到配置文件"""
    config = ConfigParser()
    config.add_section("Account")
    config.set("Account", "username", information["username"])
    config.set("Account", "password", information["password"])
    config.set("Account", "file_path", information["file_path"])
    with open(path, "w") as configfile:
        config.write(configfile)


def load_account():
    """从配置文件中加载账户信息和文件保存位置"""
    config = ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return (
        config.get("Account", "username"),
        config.get("Account", "password"),
        config.get("Account", "file_path"),
    )


def login():
    global file_path
    soup = BeautifulSoup(
        send_request("https://shequ.codemao.cn", "get", None, HEADERS).text,
        "html.parser",
    )
    pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
    USERDICT["username"], USERDICT["password"], USERDICT["file_path"] = (
        load_account() if has_config_file() else input_account()
    )
    send_request(
        "https://api.codemao.cn/tiger/v3/web/accounts/login",
        "post",
        dumps(
            {
                "identity": USERDICT["username"],
                "password": USERDICT["password"],
                "pid": pid,
            }
        ),
        headers=HEADERS,
    )

    if response.status_code == 200:
        cookies = utils.dict_from_cookiejar(response.cookies)
        cookie_str = (
            "authorization=" + cookies["authorization"] + ";acw_tc=" + cookies["acw_tc"]
        )
        print("登录成功")
        if not has_config_file():
            while True:
                USERDICT["file_path"] = input("请输入文件保存位置：")
                if path.exists(USERDICT["file_path"]):
                    try:
                        open(path.join(USERDICT["file_path"], FILE_NAME), "w+")
                    except PermissionError:
                        print("没有足够的权限读取或写入 {}".format(USERDICT["file_path"]))
                        continue
                    save_account(USERDICT, CONFIG_FILE_PATH)
                    if input("初次使用,需清除原有账户信息,是否继续?是(Y)否(Any key)") == "Y":
                        clear_oldthings()
                    return cookie_str
                else:
                    print("错误: 该路径不存在，请输入其他路径")
        elif not path.exists(path.join(USERDICT["file_path"], FILE_NAME)):
            remove(CONFIG_FILE_PATH)
            print("原配置文件信息错误,已删除,请重试")
            return None
        else:
            return cookie_str
    else:
        print(f"登录失败,错误码{response.status_code}")
        return None


def input_account():
    """为账号密码和文件保存位置输入提供交互界面"""
    get_username = input("请输入账号：")
    get_password = input("请输入密码：")
    return get_username, get_password, " "


def like_work(cookie, work_id):
    """对某个作品进行点赞"""
    send_request(
        f"https://api.codemao.cn/nemo/v2/works/{work_id}/like",
        "post",
        dumps({}),
        headers,
    )
    if response.status_code == 200:
        global like_num
        like_num += 1
        print("点赞成功  " + "点赞总数：" + str(like_num))

        return True
    else:
        print(f"点赞失败，错误代码：{response.status_code}")
        return False


def comment_work(cookie, work_id):
    """对某个作品进行评论"""
    contents = [
        "666＃°Д°",
        "加油！:O",
        "针不戳:D",
        "前排:P",
        "沙发*/ω＼*",
        "继续冲鸭！^_^",
        "排名无二OωO",
        "熊猫脸(•ㅂ•)/",
        "鸭梨山大…╭(°A°`)╮",
        "皇冠驾到~ヽ(•̀ω•́ )ゝ",
        "旋风赞美！（〜^∇^)〜",
        "小飞棍来喽(乐",
        "我方了",
        "爷青回",
        "啊这.....",
        "芜湖!起飞~",
        "不错不错",
        "吾辈楷模",
        "优雅永不过时",
        "哇~瑞斯拜!",
        "这就挺秃然的",
        "没有人比我更懂评论(赞赏",
        "奥里给!加油鸭",
        "让我康康!",
        "力挺！d(`･∀･)b",
        "我来啦！^ω^",
        "真是绝了∑(っ °Д °;)っ",
        "最好的你在前头O(∩_∩)O",
        "小板凳等你(/・ω・)/",
        "火力全开ing～^o^",
        "无敌是多么寂寞_(:3」∠)_",
        "看我破浪前行！٩(˃̶͈̀௰˂̶͈́)و",
        "感觉压力好大… `(＞＜)′",
        "金皇冠闪亮登场~ ^o^",
        "风暴赞美已开启！ヾ(^▽^*)))",
        "滚滚赞美来袭！",
        "我就问问，看谁敢回答",
        "嘿嘿嘿，看看这个，哀家有预感",
        "起飞喽，芜湖~ ^o^",
        "点赞，点赞，就很不错！",
        "你的魅力永不过时",
    ]
    emojis = [
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
    ]
    content = shielding(choice(contents))
    emoji = choice(emojis)
    send_request(
        f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment",
        "post",
        data=dumps(
            {
                "content": content,
                "emoji_content": emoji,
            }
        ),
        headers=headers,
    )
    if response.status_code == 201:
        global content_num
        content_num += 1
        print(
            "\n".join(
                [
                    "评论成功  " + "评论总数：" + str(content_num),
                    f"评论内容  {content}",
                    f"附带表情  {emoji}",
                ]
            )
        )

        return True
    else:
        print(f"评论发送失败，错误代码：{response.status_code}\n")
        return False


def write(text, name):
    with open(path.join(USERDICT["file_path"], name), "a", encoding="utf-8") as file:
        file.write(str(text) + "\n")


def check_string(stred):
    if path.exists(path.join(USERDICT["file_path"], FILE_NAME)):
        with open(path.join(USERDICT["file_path"], FILE_NAME), "r") as f:
            lines = f.readlines()

        if stred in UNDO_LIST or any(stred in line for line in lines):
            return False

    return True


def shielding(content):
    return b"\xe2\x80\xaa".decode("UTF-8").join([i for i in content])


def clear_oldthings():
    infos = 0
    while True:
        record = send_request(
            "https://api.codemao.cn/web/message-record/count", "get", None, headers
        )
        response1 = send_request(
            f"https://api.codemao.cn/web/message-record?query_type=LIKE_FORK&limit=200&offset={infos}",
            "get",
            None,
            headers,
        )
        # offset含义为抵消最新作品的前..个,返回之后的limit数量
        response2 = send_request(
            f"https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit=200&offset={infos}",
            "get",
            None,
            headers,
        )
        infos += 200
        if response1.status_code == 200:
            pass
        else:
            print(f"评论和回复清除失败,错误代码：{response1.status_code}\n")
        if response2.status_code == 200:
            pass
        else:
            print(f"点赞清除失败,错误代码：{response2.status_code}\n")

        if loads(record.text)[0]["count"] == 0 and loads(record.text)[1]["count"] == 0:
            break
    print("清除成功")


def reply_work():
    answers = (
        "这是屑猫鱼a的自动回复,不知道你在说啥(",
        "猫鱼的自动回复来喽",
        "嗨嗨嗨!这事猫鱼の自动回复鸭!",
        "猫鱼很忙oh,机器人来凑热闹（*＾＾*）",
        "猫鱼の自动回复可是个祖安软件(怕",
        "哈喽哈喽！我是猫鱼的机器人助手～",
        "我是猫鱼的小小助手，猫鱼正忙着呢，我来陪你哈",
        "对不起，猫鱼它又搞忘了时间，一定是在忙呢",
        "机器人要开始搅局了，猫鱼说忙完就过来！",
    )
    record = send_request(
        "https://api.codemao.cn/web/message-record/count", "get", None, headers
    )
    if loads(record.text)[0]["count"] >= 1:
        print("\n侦测到" + str(loads(record.text)[0]["count"]) + "个新回复\n")
        if loads(record.text)[0]["count"] > 5:
            send_request(
                "https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit={}&offset=0".format(
                    loads(record.text)[0]["count"]
                ),
                "get",
                None,
                headers,
            )
            new = send_request(
                "https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit={}&offset=0".format(
                    loads(record.text)[0]["count"]
                ),
                "get",
                None,
                headers,
            )

        else:
            new = send_request(
                "https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit=5&offset=0",
                "get",
                None,
                headers,
            )
        for infos in range(loads(record.text)[0]["count"]):
            first_reply = loads(loads(new.text)["items"][infos]["content"])["message"]
            answer = choice(answers)
            print("回复类型  {}".format(loads(new.text)["items"][infos]["type"]))
            if loads(new.text)["items"][infos]["type"] == "WORK_COMMENT":
                # WORK_COMMENT k端自己作品被别人评论
                send_request(
                    "https://api.codemao.cn/web/forums/replies/{}/comments".format(
                        first_reply["replied_id"]
                    ),
                    "post",
                    data=dumps(
                        {
                            "parent_id": first_reply["reply_id"],
                            "content": answer,
                        }
                    ),
                    headers=headers,
                )
            send_request(
                "https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                    first_reply["business_id"], first_reply["replied_id"]
                ),
                method="post",
                data=dumps(
                    {
                        "parent_id": loads(new.text)["items"][infos]["reference_id"],
                        "content": answer,
                    }
                ),
                headers=headers,
            )

            if loads(new.text)["items"][infos]["type"] == "WORK_REPLY":
                # WORK_REPLY 别人回复自己的评论
                send_request(
                    "https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                        first_reply["business_id"], first_reply["replied_id"]
                    ),
                    method="post",
                    data=dumps(
                        {
                            "parent_id": loads(new.text)["items"][infos][
                                "reference_id"
                            ],
                            "content": answer,
                        }
                    ),
                    headers=headers,
                )

            if (
                loads(new.text)["items"][infos]["type"] == "WORK_REPLY_REPLY_FEEDBACK"
                or loads(new.text)["items"][infos]["type"] == "WORK_REPLY_REPLY"
            ):
                # WORK_REPLY_REPLY_FEEDBACK 别人回复自己的回复
                # WORK_REPLY_REPLY 别人回复自己评论底下别人的回复
                print("已跳过\n")
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
                                loads(loads(new.text)["items"][infos]["content"])[
                                    "sender"
                                ]["nickname"],
                                loads(new.text)["items"][infos]["sender_id"],
                            ),
                            "回复内容  {}".format(first_reply["reply"]),
                            f"发送内容  {answer}\n",
                        ]
                    )
                )
            else:
                print(f"回复发送失败，错误代码：{response.status_code}\n")
            sleep(randint(12, 20))


def main():
    global like_num, content_num, headers
    like_num = content_num = 0
    while True:
        cookie_or_account = input("账号登录(K)&cookie(C):")
        if cookie_or_account == "K":
            cookie = login()
            if cookie:
                break
        elif cookie_or_account == "C":
            cookie_str = input("请输入cookie：")
            if like_work(cookie_str, 174408420):
                cookie = cookie_str
                break
            else:
                print("测试失败，请重新获取cookie或重试！")
        else:
            print("输入错误，请确认是否为括号中的提示词再重试!")
    headers = {
        **HEADERS,
        "cookie": cookie,
    }

    while True:
        lcr = input("仅点赞(L)&仅回复(R)点赞评论(LC)&点赞评论回复(LCR):")
        if lcr in ["L", "R", "LC", "LCR"]:
            break
        else:
            print("输入错误，请确认是否为括号中的提示词再重试!")
    while True:
        if "L" in lcr:
            new = send_request(
                "https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?offset=0&limit=50",
                "get",
                None,
                headers,
            )  # 为防止封号,limit建议调大
            _dict = loads(new.text)
            print("\n已获取{}个新作品列表".format(len(_dict["items"])))
            for infos in _dict["items"]:
                item = list(infos.items())
                if not check_string(str(item[0][1])):
                    print("已经发送过了")
                    sleep(5)
                    continue
                print(
                    "\n".join(
                        [
                            f"\n作品信息  {item[1][1]} {item[0][1]}",
                            f"作者信息  {item[5][1]} {item[3][1]}",
                        ]
                    )
                )
                like_work(cookie, item[0][1])
                if "C" in lcr:
                    if int(item[7][1]) < 50:
                        comment_work(cookie, item[0][1])
                        write(item[0][1], FILE_NAME)
                        sleep(randint(12, 20))
                    else:
                        print("不适于发送")
        if "R" in lcr:
            reply_work()
            sleep(randint(12, 20))


if __name__ == "__main__":
    main()
