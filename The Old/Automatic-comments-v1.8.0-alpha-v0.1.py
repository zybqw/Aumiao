from os import getcwd, path, remove, access, W_OK
from requests import Session, utils, post, get
from random import choice, randint
from json import dumps, loads
from bs4 import BeautifulSoup
from configparser import ConfigParser
from time import sleep
from ctypes import windll
from sys import executable

CONFIG_FILE_PATH = path.join(getcwd(), "config.ini")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
}
UNDO_LIST = ["18996184"]


def has_config_file():
    """检查是否已存在配置文件"""
    return path.isfile(CONFIG_FILE_PATH)


def save_account(username, password, file_path):
    """保存账户信息和文件保存位置到配置文件"""
    if not has_config_file():
        config = ConfigParser()
        config.add_section("Account")
        config.set("Account", "username", username)
        config.set("Account", "password", password)
        config.set("Account", "file_path", file_path)
        with open(CONFIG_FILE_PATH, "w") as configfile:
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


def check_file(file_path):
    # 检查路径是否存在
    if path.exists(file_path):
        # 检查路径是否具有写权限
        if access(file_path, W_OK):
            return True
        else:
            print("错误: 该路径不具有写权限，正在提升权限")
            windll.shell32.ShellExecuteW(None,"runas", executable, __file__, None, 1)
            if windll.shell32.IsUserAnAdmin():
                print("权限获取成功!")
                return True
            else:
                print("权限获取失败!")
                return False
    else:
        print("错误: 该路径不存在，请输入其他路径")
        return False

def login():
    global file_path
    ses = Session()
    soup = BeautifulSoup(
        ses.get("https://shequ.codemao.cn", headers=HEADERS).text, "html.parser"
    )
    pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
    username, password, file_path = (
        load_account() if has_config_file() else input_account()
    )

    response = ses.post(
        "https://api.codemao.cn/tiger/v3/web/accounts/login",
        headers=HEADERS,
        data=dumps({"identity": username, "password": password, "pid": pid}),
    )
    if response.status_code == 200:
        cookies = utils.dict_from_cookiejar(response.cookies)
        cookie_str = (
            "authorization=" + cookies["authorization"] + ";acw_tc=" + cookies["acw_tc"]
        )
        print("登录成功")
        if not has_config_file():
            while True:
                file_path = input("请输入文件保存位置：")
                if check_file(file_path):
                    save_account(username, password, file_path)
                    open(path.join(file_path, "qwq.txt"), "w")
                    return cookie_str
        elif not path.exists(path.join(file_path, "qwq.txt")):
            print(path.join(file_path, "qwq.txt"))
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
    username = input("请输入账号：")
    password = input("请输入密码：")
    return username, password, " "


def like_work(cookie, work_id):
    """对某个作品进行点赞"""
    response = post(
        f"https://api.codemao.cn/nemo/v2/works/{work_id}/like",
        headers=headers,
        data=dumps({}),
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
        "作为榜样，你表现出色！",
        "你的自然魅力永不过时",
    ]
    emojis = [
        "编程猫_666",
        "编程猫_棒",
        "编程猫_打call",
        "编程猫_加油",
        "雷电猴_哇塞",
        "魔术喵_魔术",
        "星能猫_耶",
    ]
    content = shielding(choice(contents))
    emoji = choice(emojis)
    response = post(
        f"https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment",
        headers=headers,
        data=dumps(
            {
                "content": content,
                "emoji_content": emoji,
            }
        ),
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
    with open(path.join(file_path, name), "a", encoding="utf-8") as file:
        file.write(str(text) + "\n")


def check_string(stred):
    if path.exists(path.join(file_path, "qwq.txt")):
        with open(path.join(file_path, "qwq.txt"), "r") as f:
            lines = f.readlines()

        if stred in UNDO_LIST or any(stred in line for line in lines):
            return False

    return True


def shielding(content):
    return b"\xe2\x80\xaa".decode("UTF-8").join([i for i in content])


def clear_oldthings():
    infos = 0
    while True:
        record = get(
            "https://api.codemao.cn/web/message-record/count",
            headers=headers,
        )

        response1 = get(
            f"https://api.codemao.cn/web/message-record?query_type=LIKE_FORK&limit=200&offset={infos}",  # offset含义为抵消最新作品的前..个,返回之后的limit数量
            headers=headers,
        )
        response2 = get(
            f"https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit=200&offset={infos}",
            headers=headers,
        )
        infos += 200
        if response1.status_code == 200 and response2.status_code == 200:
            pass
        else:
            print(f"评论和回复清除失败,错误代码：{response.status_code}\n")
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
    record = get(
        "https://api.codemao.cn/web/message-record/count",
        headers=headers,
    )
    if loads(record.text)[0]["count"] >= 1:
        print("\n侦测到" + str(loads(record.text)[0]["count"]) + "个新回复\n")
        if loads(record.text)[0]["count"] >= 10:
            new = get(
                "https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit={}&offset=0".format(
                    loads(record.text)[0]["count"]
                ),
                headers=headers,
            )
        else:
            new = get(
                "https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit=10&offset=0",
                headers=headers,
            )
        for infos in range(loads(record.text)[0]["count"]):
            first_reply = loads(loads(new.text)["items"][infos]["content"])["message"]
            answer = choice(answers)
            if loads(new.text)["items"][infos]["type"] == "WORK_COMMENT":
                response = post(
                    "https://api.codemao.cn/web/forums/replies/{}/comments".format(
                        first_reply["replied_id"]
                    ),
                    headers=headers,
                    data=dumps(
                        {
                            "parent_id": first_reply["reply_id"],
                            "content": answer,
                        }
                    ),
                )
            elif (
                loads(new.text)["items"][infos]["type"] == "WORK_REPLY"
            ):  # WORK_REPLY自己评论人家作品底下的,WORK_REPLY_REPLY_FEEDBACK别人回复自己的
                response = post(
                    "https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply".format(
                        first_reply["business_id"], first_reply["replied_id"]
                    ),
                    headers=headers,
                    data=dumps(
                        {
                            "parent_id": loads(new.text)["items"][infos][
                                "reference_id"
                            ],
                            "content": answer,
                        }
                    ),
                )
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
        sleep(20)


def main():
    global like_num, content_num, headers
    reply_sign = like_num = content_num = 0
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
            print("输入错误，请重试")
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
    if reply_sign == 0 and "R" in lcr:
        reply_sign = input("是否为初次使用自动回复?如果是,将清除原有服务器数据. 是(Y)否(any key)")
        if reply_sign == "Y":
            clear_oldthings()
    while True:
        if "L" in lcr:
            new = get(
                "https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?offset=0&limit=50",  # 为防止封号,limit建议调大
                headers=headers,
            )
            _dict = loads(new.text)
            print("\n已获取{}个新作品列表".format(len(_dict["items"])))
            for infos in _dict["items"]:
                item = list(infos.items())
                print(
                    "\n".join(
                        [
                            f"\n作品信息  {item[1][1]} {item[0][1]}",
                            f"作者信息  {item[5][1]} {item[3][1]}",
                        ]
                    )
                )
                like_work(cookie, item[0][1])
                sleep(10)
                if "C" in lcr:
                    if check_string(str(item[0][1])):
                        if int(item[7][1]) < 50:
                            comment_work(cookie, item[0][1])
                            write(item[0][1], "qwq.txt")
                            sleep(randint(12, 20))
                        else:
                            print("不适于发送")
                    else:
                        print("已经发送过了")
        if "R" in lcr:
            reply_work()


if __name__ == "__main__":
    main()
