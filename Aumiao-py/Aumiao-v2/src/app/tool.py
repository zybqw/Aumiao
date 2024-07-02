import json
import time
from typing import Any, Dict, List


class Process:
    def process_reject(
        self, data: List | Dict, reserve: List = None, exclude: List = None
    ) -> List | Dict:
        if reserve and exclude:
            raise ValueError(
                "请仅提供 'reserve' 或 'exclude' 中的一个参数,不要同时使用."
            )

        def filter_keys(item):
            if reserve is not None:
                return {key: value for key, value in item.items() if key in reserve}
            elif exclude is not None:
                return {key: value for key, value in item.items() if key not in exclude}

        if isinstance(data, list):
            return [filter_keys(item) for item in data]
        elif isinstance(data, dict):
            return filter_keys(data)
        else:
            raise ValueError("不支持的数据类型")

    # 对评论内容进行处理的函数
    def process_shielding(self, content: str) -> str:
        content_bytes = [item.encode("UTF-8") for item in content]
        result = b"\xe2\x80\x8b".join(content_bytes).decode("UTF-8")
        return result

    # 时间戳转换为时间
    def process_timestamp(self, times: int) -> str:
        timeArray = time.localtime(times)
        StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return StyleTime

    # 通过点分隔的键路径从嵌套字典中获取值
    def process_path(self, data: Dict, path: str) -> Any:
        keys = path.split(".")
        value = data
        for key in keys:
            value = value.get(key, {})
        return value


class File:
    # 从配置文件加载账户信息的函数
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

    # 将文本写入到指定文件的函数
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
