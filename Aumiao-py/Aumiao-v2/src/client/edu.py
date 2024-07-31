import json

import src.app.acquire as Acquire


class Edu:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 教师登录
    def teacher_login(self):
        pass

    # 创建班级
    def create_class(self, name: str):
        data = json.dumps({"name": name})
        self.acquire.send_request(
            url="https://eduzone.codemao.cn/edu/zone/class", method="post", data=data
        )
