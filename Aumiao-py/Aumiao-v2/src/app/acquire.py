import time

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from ..decorator import retry
from . import data as Data
from . import tool as Tool

session = requests.session()


class CodeMaoClient:
    def __init__(self) -> None:
        self.data = Data.CodeMaoData()
        self.tool_process = Tool.CodeMaoProcess()
        self.HEADERS = self.data.PROGRAM_DATA["HEADERS"]
        self.BASE_URL = self.data.PROGRAM_DATA["BASE_URL"]
        global session

    def send_request(
        self,
        url: str,
        method: str,
        params=None,
        data=None,
        headers=None,
        sleep=0.3,
    ):

        headers = headers or self.HEADERS
        url = url if "http" in url else f"{self.BASE_URL}{url}"
        time.sleep(sleep)
        try:
            response = session.request(
                method=method, url=url, headers=headers, params=params, data=data
            )
            response.raise_for_status()
            return response
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            print(f"网络请求异常: {err}")
            print(f"错误码: {response.status_code} 错误信息: {response.text}")
            return response

    @retry(retries=3, delay=20)
    def fetch_all_data(
        self,
        url: str,
        params: dict[str, str | bool | int],
        total_key: str = "total",
        data_key: str = "item",
        method: str = "offset",
        args: dict = {"amount": "limit", "remove": "offset"},
    ) -> list[dict]:
        initial_response = self.send_request(url=url, method="get", params=params)
        total_items = int(
            self.tool_process.process_path(initial_response.json(), total_key)  # type: ignore
        )
        items_per_page = params[args["amount"]]
        total_pages = (total_items // items_per_page) + (  # type: ignore
            1 if total_items % items_per_page > 0 else 0  # type: ignore
        )
        all_data = []
        for page in range(total_pages):
            if method == "offset":
                params[args["remove"]] = page * items_per_page
            elif method == "page":
                params[args["remove"]] = page + 1 if page != total_pages else page
            response = self.send_request(url=url, method="get", params=params)
            all_data.extend(self.tool_process.process_path(response.json(), data_key))
        return all_data

    def update_cookie(self, cookie: str):
        if isinstance(cookie, requests.cookies.RequestsCookieJar):  # type: ignore
            cookie = requests.utils.dict_from_cookiejar(cookie)
        elif isinstance(cookie, dict):
            pass
        else:
            raise ValueError("不支持的数据类型")
        session.cookies.update(cookie)  # type: ignore
        return True
