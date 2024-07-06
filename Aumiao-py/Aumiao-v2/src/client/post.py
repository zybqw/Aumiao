from typing import List

import src.app.acquire as acquire
import src.app.tool as tool


class Post:
    def __init__(self) -> None:
        self.acquire = acquire.CodeMaoClient()
        self.tool = tool.CodeMaoProcess()

    def get_posts_detials(self, ids: int | List):
        if isinstance(ids, int):
            params = {"ids": ids}
        elif isinstance(ids, List):
            params = {"ids": ",".join(map(str, ids))}
        response = self.acquire.send_request(
            url="/web/forums/posts/all", method="get", params=params
        )
        data = self.tool.process_reject(
            data=response.json(),
            reserve=["id", "title", "content", "created_at", "user"],
        )

        return data
