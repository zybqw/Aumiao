import json
from typing import Dict


class CodeMaoFile:
    # 从配置文件加载账户信息
    def file_load(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    # 检查文件
    def check_file(self, path: str) -> bool:
        try:
            with open(path, "r"):
                return True
        except IOError:
            return False

    # 将文本写入到指定文件
    def write(
        self,
        path: str,
        text: str | Dict,
        type: str = "str",
        method: str = "w",
    ) -> None:
        with open(path, mode=method, encoding="utf-8") as file:
            if type == "str":
                file.write(text + "\n")
            elif type == "dict":
                file.write(json.dumps(text, ensure_ascii=False, indent=4))
            else:
                raise ValueError("不支持的写入方法")
