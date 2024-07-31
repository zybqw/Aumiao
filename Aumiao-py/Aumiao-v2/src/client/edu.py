import json
from typing import Literal

import src.app.acquire as Acquire
import src.client.community as community


class Edu:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 教师登录
    def teacher_login(self):
        pass

    # 创建班级
    def create_class(self, name: str):
        data = json.dumps({"name": name})
        response = self.acquire.send_request(
            url="https://eduzone.codemao.cn/edu/zone/class", method="post", data=data
        )
        return response.json()

    # 获取班级
    def get_classes(
        self, limit: int = 15, method: Literal["detail", "simple"] = "simple"
    ):
        time_stamp = community.Obtain().get_timestamp()["data"]
        params = {"page": 1, "TIME": time_stamp}
        reminder = method if method == "simple" else ""
        url = f"{"https://eduzone.codemao.cn/edu/zone/classes"}{reminder}"
        classes = self.acquire.fetch_all_data(
            url=url,
            params=params,
            data_key="items",
            method="page",
            args={"amount": "limit", "remove": "page"},
        )
        return classes

    # 删除班级
    def delete_class(self, id: int):
        time_stamp = community.Obtain().get_timestamp()["data"]
        params = {"TIME": time_stamp}
        response = self.acquire.send_request(
            url=f"https://eduzone.codemao.cn/edu/zone/class/{id}",
            method="delete",
            params=params,
        )
        return response.status_code == 204

    # 班级内新建学生账号
    def create_student(self, name: list[str], class_id: int):
        data = json.dumps({"student_names": name})
        response = self.acquire.send_request(
            url=f"https://eduzone.codemao.cn/edu/zone/class/{class_id}/students",
            method="post",
            data=data,
        )
        return response.status_code == 200
