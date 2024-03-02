from os import getcwd, path, remove, access, W_OK
from requests import Session, utils, post, get
from random import choice, randint
from json import dumps, loads
from bs4 import BeautifulSoup
from configparser import ConfigParser
from time import sleep

CONFIG_FILE_PATH = path.join(getcwd(), "config.ini")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
}


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
                file_dir = input("请输入qwq.txt文件保存位置：")
                file_path = path.join(file_dir, "qwq.txt")

                # 检查路径是否存在
                if path.exists(file_dir):
                    # 检查路径是否具有写权限
                    if access(file_dir, W_OK):
                        save_account(username, password, file_path)
                        break
                    else:
                        print("错误: 该路径不具有写权限，请输入其他路径")
                else:
                    print("错误: 该路径不存在，请输入其他路径")

        return cookie_str
    else:
        print("不能登录编程猫，请重试")
        if has_config_file():
            remove(CONFIG_in)
            print("config.ini原有配置已成功删除！")
        return None


def input_account():
    """为账号密码和文件保存位置输入提供交互界面"""
    username = input("请输入账号：")
    password = input("请输入密码：")
    return username, password, " "


def like_work(cookie, work_id):
    """对某个作品进行点赞"""
    headers = {
        **HEADERS,
        "cookie": cookie,
    }
    response = post(
        f"https://api.codemao.cn/nemo/v2/works/{work_id}/like",
        headers=headers,
        data=dumps({}),
    )
    if response.status_code == 200:
        print(f"点赞成功")
        global like_num
        like_num += 1
        return True
    else:
        print(f"点赞失败，错误代码：{response.status_code}")
        return False


def comment_work(cookie, work_id):
    """对某个作品进行评论"""
    contents = ["666＃°Д°", "加油！:O", "针不戳:D", "前排:P", "沙发*/ω＼*"]
    emojis = [
        "编程猫_666",
        "编程猫_棒",
        "编程猫_打call",
        "编程猫_加油",
        "雷电猴_哇塞",
        "魔术喵_魔术",
        "星能猫_耶",
    ]
    headers = {
        **HEADERS,
        "cookie": cookie,
    }
    content = choice(contents)
    emoji = shielding(choice(emojis))
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
        print(
            "\n".join(
                [
                    f"评论成功",
                    f"评论内容  {content}",
                    f"附带表情  {emoji}",
                ]
            )
        )
        global content_num
        content_num += 1
        return True
    else:
        print(f"评论发送失败，错误代码：{response.status_code}\n")
        return False


def write(text):
    with open(file_path, "a+", encoding="utf-8") as file:
        file.write(str(text) + "\n")


def check_string(stred):
    if path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        if stred in ["18996184"] or any(stred in line for line in lines):
            return False

    return True


def shielding(content):
    return b"\xe2\x80\xaa".decode("UTF-8").join([i for i in content])


def main():
    global like_num, content_num
    like_num = content_num = 0
    while True:
        cookie_or_account = input("账号登录(K)&cookie(C):")
        if cookie_or_account == "K":
            cookie = login()
            if cookie is not None:
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

    while True:
        like_or_content = input("仅点赞(L)&点赞评论(A):")
        if like_or_content == "L" or like_or_content == "A":
            break
        else:
            print("输入错误，请重试!")

    while True:
        try:
            new = get(
                "https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?offset=0&limit=20"
            )
            _dict = loads(new.text)
            print("\n已获取新作品列表")
            print("点赞总数：" + str(like_num))
            if like_or_content == "A":
                print("评论总数：" + str(content_num))
            for infos in _dict["items"]:
                item = list(infos.items())
                try:
                    print(
                        "\n".join(
                            [
                                f"\n作品编号  {item[0][1]}",
                                f"作者昵称  {item[5][1]}",
                                f"作品名称  {item[1][1]}",
                            ]
                        )
                    )
                    like_work(cookie, item[0][1])
                    if like_or_content == "A":
                        if check_string(str(item[0][1])):
                            if int(item[7][1]) < 50:
                                comment_work(cookie, item[0][1])
                                write(item[0][1])
                                sleep_time = randint(12, 16)
                                sleep(sleep_time)
                            else:
                                print("不适于发送")
                        else:
                            print("已经发送过了")
                except KeyboardInterrupt:
                    exit_num = True
                    break
                except Exception as e:
                    print("程序发生异常: ", e)
                    sleep(5)  # 间隔时间
                    continue
            if exit_num == True:
                print("用户中断运行")
                exit()
        except Exception as e:
            sleep(5)
            print("程序发生异常: ", e)


if __name__ == "__main__":
    main()
