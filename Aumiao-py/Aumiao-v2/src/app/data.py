import os

import src.app.file as File


class CodeMaoData:
    CONFIG_FILE_PATH: str = os.path.join(os.getcwd(), "data.json")

    def __init__(self):
        data = File.CodeMaoFile.file_load(self.CONFIG_FILE_PATH)

        self.PROGRAM_DATA.update(data["PROGRAM_DATA"])
        self.USER_DATA.update(data["USER_DATA"])

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
