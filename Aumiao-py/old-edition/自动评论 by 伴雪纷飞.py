from datetime import *
from requests import *
from time import sleep
from random import choice
from json import loads,dumps

def check_string():
    with open('qwq.txt', 'r',encoding='utf-8') as f:
        lines = f.readlines()
    for line_number in lines:
        if str(item[0][1]) in line_number:
            return True
    if not str(item[3][1]) in [18996184]:
        return False
    else:
        return True
    f.close()
#遍历列表

cookie='__ca_uid_key__=cd1e2e04-3d0e-4537-ad93-84f46eeebf78; TY_SESSION_ID=28cbb524-cd5\
6-414e-b1b3-49b82386092e; authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJD\
b2RlbWFvIEF1dGgiLCJ1c2VyX3R5cGUiOiJzdHVkZW50IiwiZGV2aWNlX2lkIjowLCJ1c2VyX2lkIjoxMjc3MDExN\
CwiaXNzIjoiQXV0aCBTZXJ2aWNlIiwicGlkIjoiNjVlZENUeWciLCJleHAiOjE2Nzk0ODk4MDgsImlhdCI6MTY3NTY\
wMTgwOCwianRpIjoiMzc5NzMxODAtNjhmNC00MTVhLTg2NjMtMmE2YjU2OTg4MjBiIn0.YYwuBTkaNYLxyXFynyjLzz2XVhJuROYCcseEiacBAx8'
i=0
while True:
    sleep(5)
    new = get('https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?offset=0&limit=10')#limit获取数量
    print('\n'+"@zybqw or 爱吃猫的鱼 or 猫鱼")
    _dict = loads(new.text)
    print(new.text+'\n')
    print('='*200)
    for infos in _dict['items']:
        item = list(infos.items())
        print('\n'+str(item))
        if check_string():
            print('\n'+'已存在或禁止发送')
        else:
            i+=1#简化写法
            headers ={
                "Content-Type": "application/json",
                "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
                'cookie': cookie
                     }
            sentents = (
                '666＃°Д°',
                '加油！:O',
                '针不戳:D',
                '前排:P',
                '沙发*/ω＼*'
                        )
            print('\n'+'不存在')
            print('作品编号          '+str(item[0][1]))
            print('作品名称          '+str(item[1][1]))
            print('作者编号          '+str(item[3][1]))
            print('作者昵称          '+str(item[5][1]))
            print('评论数量          '+str(item[6][1]))
            print('点赞数量          '+str(item[7][1]))
            item=list(infos.items())
            content=choice(sentents).format(work_name=item[1][1],nick_name=item[5][1])
            try:
                p=post(r'''https://api.codemao.cn/creation-tools/v1/works/{}/comment'''.format(item[0][1]),
                    headers=headers, 
                    data=dumps({'content': content}))#评论
                p = post(r'https://api.codemao.cn/nemo/v2/works/{}/like'.format(item[0][1]),
                    headers=headers,
                    data=dumps({}))#点赞
                print(datetime.now())
                print('已发送评论'+str(i)+'条')
                with open('qwq.txt', 'a+', encoding='utf-8') as file:
                    file.write('\n'.join(['作品编号    '+format(item[0][1]), '作品名称    '+format(item[1][1]),'作者编号    '+format(item[3][1]), '作者昵称    '+format(item[5][1]),str(datetime.now())]))
                    file.write('\n' + '=' * 50 + '\n')
                    file.close()
            except:
                pass
            sleep(12)#一小时三百个,每分钟5个,12秒一个(忽略计算和网络延迟,理论上是最高速度
        print('*'*100)

#笔记
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
#not是 “非” ；and是 “与” ；or是 “或” （可以用数学去理解)
#1、not True = False 或者 not False = True (非真就是假，非假即真)
#2、and是一假则假，两真为真，两假则假
#3、or是一真即真，两假即假，两真则真
#优先级是 not > and > or
