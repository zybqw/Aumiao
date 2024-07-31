import os

from . import file as File
from .decorator import singleton

DATA_FILE_PATH: str = os.path.join(os.getcwd(), "data/" "data.json")
CACHE_FILE_PATH: str = os.path.join(os.getcwd(), "data/" "cache.json")


@singleton
class CodeMaoData:
    def __init__(self) -> None:
        data = File.CodeMaoFile().file_load(path=DATA_FILE_PATH, type="json")

        self.PROGRAM_DATA.update(data["PROGRAM_DATA"])  # type: ignore
        self.USER_DATA.update(data["USER_DATA"])  # type: ignore
        self.ACCOUNT_DATA.update(data["ACCOUNT_DATA"])  # type: ignore

    PROGRAM_DATA = {
        "HEADERS": {
            "Content-Type": "",
            "User-Agent": "",
        },
        "BASE_URL": "",
        "SLOGAN": "",
        "SAVE_PATH": "",
    }

    USER_DATA = {
        "black_room": {
            "user": [],
            "work": [],
            "post": [],
        },
        "comments": [],
        "emojis": [],
        "answers": [],
        "replies": [],
        "ads": [],
    }
    ACCOUNT_DATA = {
        "identity": "",
        "password": "",
        "id": "",
        "nickname": "",
        "description": "",
        "create_time": "",
        "author_level": "",
    }
