import requests
from json import loads, dumps
from bs4 import BeautifulSoup
import random
import time
zplb = []
zh = str(input('请输入账号:'))
mm = str(input('请输入密码'))
ca = 0
while True:
    #这两个参数分别是cookies 和 作品id
    def zpdz(cookies, zpid):
        ses = requests.session()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            'cookie': cookies
        }
        p = requests.post('https://api.codemao.cn/nemo/v2/works/' +
                        str(zpid) + '/like', headers=headers, data=dumps({}))
        return p.status_code

    #三个参数分别是 cookies 作品id 评论内容
    def hfzp(cookies, zpid, nr):
        ses = requests.session()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHtmL, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            'cookie': cookies
        }
        p = requests.post('https://api.codemao.cn/creation-tools/v1/works/' + str(zpid) +
                        '/comment', headers=headers, data=dumps({'emoji_content': "", 'content': nr}))
        return p.status_code


    fxses = requests.session()
    fxheaders = {"Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHtmL, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    fxsoup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=fxheaders).text, 'html.parser')
    fxpid = loads(fxsoup.find_all("script")[0].string.split("=")[1])['pid']
    fxa = fxses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=fxheaders,data=dumps({"identity": zh, "password": mm, "pid": fxpid}))
    if fxa.status_code == 200:
        fxc = fxa.cookies
        fxcookies = requests.utils.dict_from_cookiejar(fxc)
        fxcookiess = 'authorization=' + fxcookies['authorization'] + ';acw_tc=' + fxcookies['acw_tc']
        pxcookie = fxcookiess

    else:
        exit("不能登录编程猫")
    url = 'https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?work_origin_type=ORIGINAL_WORK&offset=0&limit=20'
    r = requests.get(url)
    xx = r.json()['items']
    for i in range(0,len(xx)):
        work_id = xx[i]['work_id']
        work_name = xx[i]['work_name']
        nickname = xx[i]['nickname']
        print('作品信息 丨 作品ID : ' + str(work_id) + '    作品名称 : ' + str(work_name) + '    作者是 : ' + nickname)
        if work_id not in zplb:
            if zpdz(pxcookie,work_id) == 200:
                print('点赞成功')
                ca += 1
            else:
                print('点赞失败')
            
            zplb.append(work_id)
            
        else:
            print('已经点赞过了')
            
        print('已点赞 : ' + str(ca) + ' 次')
        print('')
