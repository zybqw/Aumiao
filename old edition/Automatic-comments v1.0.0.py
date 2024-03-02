import os
from requests import *
from time import sleep
from random import choice
from json import loads, dumps
from bs4 import BeautifulSoup
from datetime import datetime
from configparser import ConfigParser


def check_config_file():  # 获取当前工作目录
    current_path = os.getcwd()  # 拼接config.ini文件路径
    config_path = os.path.join(current_path, "config.ini")  # 判断文件是否存在
    if os.path.isfile(config_path):
        return True
    else:
        return False


def check_string():
    try:
        with open("qwq.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line_number in lines:
            if str(item[0][1]) in line_number:
                return True
        if str(item[3][1]) in [18996184]:
            return True
        else:
            return False
        f.close()
    except:
        return False


def Shielding(content):
    return b"\xe2\x80\xaa".decode("UTF-8").join([i for i in content])  # 屏蔽词转换(可选部分


awa = []
content_num = 0
like_num = 0
while True:
    lc_or_lk = str(input("账号登录(K)&cookie(C)"))
    if lc_or_lk == "K":
        if not check_config_file():
            username = str(input("请输入账号:"))
            password = str(input("请输入密码:"))
        else:
            print("侦测到已有配置")
            config = ConfigParser()
            config.read("config.ini")

            username = config.get("Account", "username")
            password = config.get("Account", "password")
        ses = session()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46",
        }
        soup = BeautifulSoup(
            get("https://shequ.codemao.cn", headers=headers).text, "html.parser"
        )
        pid = loads(soup.find_all("script")[0].string.split("=")[1])["pid"]
        a = ses.post(
            "https://api.codemao.cn/tiger/v3/web/accounts/login",
            headers=headers,
            data=dumps({"identity": username, "password": password, "pid": pid}),
        )
        if a.status_code == 200:
            c = a.cookies
            cookies = utils.dict_from_cookiejar(c)
            cookiess = (
                "authorization="
                + cookies["authorization"]
                + ";acw_tc="
                + cookies["acw_tc"]
            )
            cookie = cookiess
            print("登录成功!")
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46",
                "cookie": cookie,
            }
            if not check_config_file():
                config = ConfigParser()
                config.add_section("Account")
                config.set("Account", "username", username)
                config.set("Account", "password", password)
                with open("config.ini", "w") as configfile:
                    config.write(configfile)
            break
        else:
            print("不能登录编程猫,请重试")
            if check_config_file():
                os.remove("config.ini")
                print("config.ini原有配置已成功删除！")

    elif lc_or_lk == "C":
        cookie = str(input("请输入cookie:"))
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46",
            "cookie": cookie,
        }
        p = post(
            r"https://api.codemao.cn/nemo/v2/works/{}/like".format(174408420),  # 夹带私货(
            headers=headers,
            data=dumps({}),
        )
        if p.status_code == 200:
            print("测试成功!")
            break
        else:
            print("测试失败,请重新获取cookie或重试!")
    else:
        print("输入错误,请重试!")
while True:
    like_or_content = str(input("仅点赞(L)&点赞评论(A):"))
    if like_or_content == "L" or like_or_content == "A":
        break
    else:
        print("输入错误,请重试!")
        pass
while True:
    if like_or_content == "A":
        sleep_time = input("评论间隔时间(为防止封号,已经间隔12s)(按秒计):")
        try:
            sleep_time = float(sleep_time)
            break
        except:
            print("输入错误!请重新输入.")
    else:
        break

while True:
    new = get(
        "https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?offset=0&limit=20"
    )  # limit获取数量
    print("\n" + "@zybqw or 猫鱼")
    _dict = loads(new.text)
    print(new.text + "\n")
    print("=" * 200)
    for infos in _dict["items"]:
        item = list(infos.items())
        print("\n" + str(item))
        sentents = ("666＃°Д°", "加油！:O", "针不戳:D", "前排:P", "沙发*/ω＼*")
        picture = (
            "编程猫_666",
            "编程猫_棒",
            "编程猫_打call",
            "编程猫_加油",
            "雷电猴_哇塞",
            "魔术喵_魔术",
            "星能猫_耶",
        )
        emoji = choice(picture)
        print("作品编号          " + str(item[0][1]))
        print("作品名称          " + str(item[1][1]))
        print("作者编号          " + str(item[3][1]))
        print("作者昵称          " + str(item[5][1]))
        print("评论数量          " + str(item[6][1]))
        print("点赞数量          " + str(item[7][1]))
        item = list(infos.items())
        content = choice(sentents).format(
            work_name=item[1][1], nick_name=item[5][1]
        )  # 这里的评论中如果有列表中的内容,就会通过format导入,如{nick_name}
        p = post(
            r"https://api.codemao.cn/nemo/v2/works/{}/like".format(item[0][1]),
            headers=headers,
            data=dumps({}),
        )  # 点赞
        print(datetime.now())
        if str(item[0][1]) not in awa:
            if p.status_code == 200:
                print("点赞成功")
                sleep(2)
                like_num += 1
            else:
                print("点赞失败,error code:" + str(p.status_code))
            print("点赞了" + str(like_num) + "次")
            awa.append(str(item[0][1]))
        else:
            print("已经点赞过了")
        if like_or_content == "A":
            if check_string() or int(item[7][1]) > 50:  # 点赞大于50或已存在不发送
                print("\n" + "已存在或禁止发送")
            else:
                print("\n" + "不存在")
                p = post(
                    r"https://api.codemao.cn/creation-tools/v1/works/{}/comment".format(
                        item[0][1]
                    ),
                    headers=headers,
                    data=dumps(
                        {
                            "content": content,
                            "emoji_content": emoji,
                        }
                    ),
                )  # 评论
                content_num += 1
                print("已发送评论" + str(content_num) + "条")
                print("评论内容    " + str(content))
                print("表情内容    " + str(emoji))
                with open("qwq.txt", "a+", encoding="utf-8") as file:
                    file.write(
                        "\n".join(
                            [
                                "作品编号    " + format(item[0][1]),
                                "作品名称    " + format(item[1][1]),
                                "作者编号    " + format(item[3][1]),
                                "作者昵称    " + format(item[5][1]),
                                "评论内容    " + str(content),
                                "表情内容    " + str(emoji),
                                str(datetime.now()),
                            ]
                        )
                    )
                    file.write("\n" + "=" * 50 + "\n")
                    file.close()
                sleep(12)  # 一小时三百个,每分钟5个,12秒一个(忽略计算和网络延迟,理论上是最高速度
                sleep(sleep_time)
        print("*" * 100)

# 笔记
#   r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
#   w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
#   a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
#   rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
#   wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
#   ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
#   r+	打开一个文件用于读写。文件指针将会放在文件的开头。
#   w+	打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
#   a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
#   rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
#   wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
#   ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。

#   not x	    if x is false,then True,else False	   1
#   x and y	    if x is false,then x,else y	           2
#   x or y	    if x is false,then y,else x	           3
# not是 “非” ；and是 “与” ；or是 “或” （可以用数学去理解)
# 1、not True = False 或者 not False = True (非真就是假，非假即真)
# 2、and是一假则假，两真为真，两假则假
# 3、or是一真即真，两假即假，两真则真
# 优先级是 not > and > or
