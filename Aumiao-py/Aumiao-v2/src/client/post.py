from typing import List

import src.app.acquire as acquire


class Post:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()

    def get_posts_detials(self, ids: int | List):
        if isinstance(ids, int):
            params = {"ids": ids}
        elif isinstance(ids, List):
            params = {"ids": ",".join(map(str, ids))}
        response = self.acquire.send_request(
            url="/web/forums/posts/all", method="get", params=params
        )
        return response.json()
