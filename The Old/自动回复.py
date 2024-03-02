from requests import *
from json import loads, dumps
from random import choice
from time import sleep
cookie = r'__ca_uid_key__=cd1e2e04-3d0e-4537-ad93-84f46eeebf78; TY_SESSION_ID=28cbb524-cd56-414e-b1b3-49b82386092e; authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDb2RlbWFvIEF1dGgiLCJ1c2VyX3R5cGUiOiJzdHVkZW50IiwiZGV2aWNlX2lkIjowLCJ1c2VyX2lkIjoxMjc3MDExNCwiaXNzIjoiQXV0aCBTZXJ2aWNlIiwicGlkIjoiNjVlZENUeWciLCJleHAiOjE2Nzk0ODk4MDgsImlhdCI6MTY3NTYwMTgwOCwianRpIjoiMzc5NzMxODAtNjhmNC00MTVhLTg2NjMtMmE2YjU2OTg4MjBiIn0.YYwuBTkaNYLxyXFynyjLzz2XVhJuROYCcseEiacBAx8'
headers = {
    "Content-Type": "application/json",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
    'cookie': cookie
}
sentents = (
    '有什么事情可以到我的最新作品的评论区去说oh，有什么事加QQ3611198191'
)
while True:
    new = get('https://api.codemao.cn/web/message-record/count', headers=headers)
    print(new.text)
    if loads(new.text)[0]['count']>=1:
        print('有新内容')
        file = open('awa.txt', 'a')
        new = get(
            'https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit=101&offset=0',headers=headers)
        first_reply = loads(loads(new.text)['items'][0]['content'])['message']
        print(first_reply)
        try:
            url="https://api.codemao.cn/web/forums/replies/{}/comments".format(first_reply['replied_id'])
            p=post(url, headers=headers, data=dumps(
                {"parent_id": first_reply['reply_id'], "content": choice(sentents)}))

        except:
            pass
        file.close()
    sleep(4.01)
