import json
from typing import Literal

from .decorator import singleton


@singleton
class CodeMaoFile:
    # 检查文件
    def check_file(self, path: str) -> bool:
        try:
            with open(path, "r"):
                return True
        except IOError as err:
            print(err)
            return False

    def validate_json(self, json_string):
        try:
            data = json.loads(json_string)
            return data
        except ValueError as err:
            print(err)
            return False

    # 从配置文件加载账户信息
    def file_load(self, path, type: Literal["txt", "json"]) -> dict | str:
        self.check_file(path=path)
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
            if type == "json":
                return json.loads(data) if data else {}
            if type == "txt":
                return data
            else:
                raise ValueError("不支持的读取方法")

    # 将文本写入到指定文件
    def write(
        self,
        path: str,
        text: str | dict,
        type: str = "str",
        method: str = "w",
    ) -> None:
        self.check_file(path)
        with open(path, mode=method, encoding="utf-8") as file:
            if type == "str":

                file.write(text + "\n")  # type: ignore
            elif type == "dict":
                file.write(
                    json.dumps(text, ensure_ascii=False, indent=4, sort_keys=False)
                )
            else:
                raise ValueError("不支持的写入方法")
