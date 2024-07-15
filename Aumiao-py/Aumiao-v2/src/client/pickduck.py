import json

import src.app.acquire as Acquire


class PickDuck:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    def cookieout(self, cookies):
        data = json.dumps({"cookie": cookies, "do": "apply"})
        response = self.acquire.send_request(
            url="https://shequ.pgaot.com/?mod=bcmcookieout", method="post", data=data
        )
        return response.json()
