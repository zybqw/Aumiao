import json

import src.app.acquire as Acquire

version = "2024.7.21"

HEADERS = Acquire.CodeMaoClient().HEADERS
docs = "https://help.aliyun.com/zh/dashscope/developer-reference/use-qwen-by-api"


class Dashscope:
    def __init__(self) -> None:
        self.acquire = Acquire.CodeMaoClient()
        self.HEADERS = HEADERS

    def set_key(self, api_key: str):
        self.HEADERS["Authorization"] = f"Bearer {api_key}"

    def chat(
        self,
        method: str,
        modal: str,
        message: list = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好啊，我是通义千问。"},
            {"role": "user", "content": "你有哪些技能？"},
        ],
        multiple_assistant_message: list = [],
        more={
            "stream": False,
            "extra_body": {"enable_search": True},
            # 更多参数详见文档
        },
    ):
        if method == "single":
            pass
        elif method == "multiple":
            if multiple_assistant_message == []:
                raise ValueError("multiple_assistant_message不能为空")
            if multiple_assistant_message[-1]["role"] != "user":
                raise ValueError("messages中最后一个元素的role必须为user")

        data = json.dumps(
            {
                "model": modal,
                "messages": message,
                **more,
            }
        )
        result = self.acquire.send_request(
            url="https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            method="post",
            data=data,
        )
        return result
