/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const request = require("request")

function promise(cb) {
    return new Promise(cb)
}


const CodemaoApi = class {
    /*
     =======================
              主类
     ========================
     */
    static baseUrl = "https://api.codemao.cn"
    static headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }

    static setCookie(cookie) {
        this.headers.cookie = cookie
    }

    /*
     =======================
              子类
     ========================
     */

    /**
     * 用户逻辑
     */
    static User = class {

    }
    /**
     * 作品逻辑
     */
    static Work = class {
        static like(workId, unlike) {
            return promise((r) => request[unlike ? "delete" : "post"](`${CodemaoApi.baseUrl}/nemo/v2/works/${workId}/like`, {headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(true, body)
                r(false)
            }))
        }
    }
    /**
     * 作品_评论区逻辑
     */
    static WorkComment = class {

    }
}

exports.CodemaoApi = CodemaoApi
