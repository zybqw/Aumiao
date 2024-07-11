import requests

import src

timestamp = src.client_community_obtain.get_timestamp()["data"]

response = src.client_community_login.login_v3(identity="173", timestamp=timestamp)
ticket = response["ticket"]

response = src.client_community_login.login_security(
    identity=173, password="CO", ticket=ticket
)
token = response["auth"]["token"]

src.client_community_login.logout()


pid = "65edCTyg"
HEADERS = (
    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    },
)
response = src.app_acquire.send_request(
    url="https://shequ.codemao.cn/",
    method="get",
)
aliyungf_tc = response.cookies.get_dict()
print(aliyungf_tc)

response = src.app_acquire.send_request(
    url="/web/banners/all?type=OFFICIAL",
    method="get",
)
aliyungf_tc = response.cookies.get_dict()
print(aliyungf_tc)


cookie_dict = {**{"authorization": token}, **aliyungf_tc}

cookies = requests.utils.cookiejar_from_dict(cookie_dict)
response = src.client_community_login.login(method="cookie", cookies=str(cookies))
