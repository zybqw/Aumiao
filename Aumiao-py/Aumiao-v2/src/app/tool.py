import time
from typing import Any, Dict, List


class CodeMaoProcess:
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
    def process_timestamp(self, timestamp: int) -> str:
        timeArray = time.localtime(timestamp)
        StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return StyleTime

    # 通过点分隔的键路径从嵌套字典中获取值
    def process_path(self, data: Dict, path: str) -> Any:
        keys = path.split(".")
        value = data
        for key in keys:
            value = value.get(key, {})
        return value

    # 将cookie转换为headers中显示的形式
    def process_cookie(self, cookie):
        cookie_str = "; ".join([f"{key}={value}" for key, value in cookie.items()])
        return cookie_str


class CodeMaoRoutine:
    def get_timestamp(self):
        timestamp = time.time()
        return timestamp

    def print_changes(self, before_data, after_data, keys):
        for key in keys:
            if key in before_data and key in after_data:
                change = after_data[key] - before_data[key]
                print(f"{key} 改变 {change} 个")
            else:
                print(f"{key} 没有找到")
