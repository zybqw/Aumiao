import os

from . import file as File

CONFIG_FILE_PATH: str = os.path.join(os.getcwd(), "data/" "data.json")


class CodeMaoData:

    def __init__(self):
        data = File.CodeMaoFile().file_load(CONFIG_FILE_PATH)

        self.PROGRAM_DATA.update(data["PROGRAM_DATA"])
        self.USER_DATA.update(data["USER_DATA"])
        self.ACCOUNT_DATA.update(data["ACCOUNT_DATA"])

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
        "blackroom": {
            "user": [],
            "work": [],
            "post": [],
        },
        "comments": [],
        "emojis": [],
        "anwsers": [],
        "replies": [],
        "ads": [],
    }
    ACCOUNT_DATA = {
        "identity": "",
        "password": "",
        "id": "",
        "nickname": "",
        "descrption": "",
        "creat_time": "",
        "author_level": "",
    }
