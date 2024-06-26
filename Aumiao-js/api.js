/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const request = require("request")

const CodemaoApi = class {
    static baseUrl = "https://api.codemao.cn"
    static headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }
}

CodemaoApi.User = class {

}

CodemaoApi.Work = class {

}

CodemaoApi.WorkRoom = class {

}

module.exports = CodemaoApi
