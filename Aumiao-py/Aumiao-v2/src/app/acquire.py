from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

from ..decorator import retry
from . import data as Data
from . import tool as Tool

session = requests.session()


class CodeMaoClient:
    def __init__(self) -> None:
        self.data = Data.CodeMaoData()
        self.tool = Tool.CodeMaoProcess()
        self.HEADERS = self.data.PROGRAM_DATA["HEADERS"]
        self.BASE_URL = self.data.PROGRAM_DATA["BASE_URL"]
        global session

    @retry(retry=3, delay=5)
    def send_request(
        self,
        url: str,
        method: str,
        params: Optional[Dict] = None,
        data: Any = None,
        headers: Dict = None,
    ) -> Optional[Any]:
        headers = headers or self.HEADERS
        url = f"{self.BASE_URL}{url}"
        try:
            response = session.request(
                method=method, url=url, headers=headers, params=params, data=data
            )
            response.raise_for_status()
            return response
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            print(response.json())
            print(f"网络请求异常: {err}")
            return None

    def fetch_all_data(
        self,
        url: str,
        params: Dict[str, any],
        total_key: str,
        data_key: str,
        method: str = "offset",
        args: Dict = {"limit": "limit", "offset": "offset"},
    ) -> List[Dict]:
        initial_response = self.send_request(url=url, method="get", params=params)
        total_items = int(self.tool.process_path(initial_response.json(), total_key))
        items_per_page = params[args["limit"]]
        total_pages = (total_items // items_per_page) + (
            1 if total_items % items_per_page > 0 else 0
        )
        all_data = []
        for page in range(total_pages):
            if method == "offset":
                params[args["offset"]] = page * items_per_page
            elif method == "page":
                params[args["offset"]] = page + 1 if page != total_pages else page
            response = self.send_request(url=url, method="get", params=params)
            all_data.extend(self.tool.process_path(response.json(), data_key))
        return all_data

    def update_cookie(self, cookie: str):
        _cookie = requests.utils.dict_from_cookiejar(cookie)
        session.cookies.update(_cookie)
        return True
