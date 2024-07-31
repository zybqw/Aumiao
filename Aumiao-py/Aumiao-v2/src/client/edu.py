import json
from typing import Literal

import src.app.acquire as Acquire
import src.client.community as community


class Motion:
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

    # 重置密码
    def reset_password(self, stu_id: list[int]):
        data = json.dumps({"student_id": stu_id})
        response = self.acquire.send_request(
            url="https://eduzone.codemao.cn/edu/zone/students/password",
            method="patch",
            data=data,
        )
        return response.status_code == 200

    # 删除班级内学生
    def remove_student(self, stu_id: int):
        data = json.dumps({})
        response = self.acquire.send_request(
            url=f"https://eduzone.codemao.cn/edu/zone/student/remove/{stu_id}",
            method="post",
            data=data,
        )
        return response.status_code == 200


class Obtain:

    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()

    # 获取所有班级
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

    # 获取删除学生记录
    def get_record_del(self):
        time_stamp = community.Obtain().get_timestamp()["data"]
        params = {"page": 1, "limit": 10, "TIME": time_stamp}
        records = self.acquire.fetch_all_data(
            url="https://eduzone.codemao.cn/edu/zone/student/remove/record",
            params=params,
            data_key="items",
            method="page",
            args={"amount": "limit", "remove": "page"},
        )
        return records

    # 获取班级内全部学生
    def get_student(self, invalid: int = 1):
        # invalid为1时为已加入班级学生，为0则反之
        data = json.dumps({"invalid": invalid})
        params = {"page": 1, "limit": 100}
        students = self.acquire.fetch_all_data(
            url="https://eduzone.codemao.cn/edu/zone/students",
            params=params,
            data=data,
            fetch_method="post",
            data_key="items",
            method="page",
            args={"amount": "limit", "remove": "page"},
        )
        return students