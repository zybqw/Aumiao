/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const request = require("request")

function promise(cb) {
    return new Promise(cb)
}

function stringToJson(s) {
    if (s instanceof Object)
        return s
    return JSON.parse(s)
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

    static setCookieToken(token) {
        this.headers.cookie = `authorization=${token}`
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
        /**
         * Login your account
         * @param { String } account
         * @param { String } password
         * @returns { Promise<String> } token
         */
        static getToken(usr, psw) {
            return promise((r) => request.post(`${CodemaoApi.baseUrl}/tiger/v3/web/accounts/login`, {json: {
                identity: usr,
                password: psw,
                pid: "65edCTyg", // 写死的, 不会变动
            }, headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(stringToJson(body).auth.token)
                r(null)
            }))
        }
        /**
         * Get my details
         * @returns { Promise<Object> } json
         */
        static getMyDetails() {
            return promise((r) => request.get(`${CodemaoApi.baseUrl}/web/users/details`, {headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(stringToJson(body))
                r(null)
            }))
        }
    }
    /**
     * 作品逻辑
     */
    static Work = class {
        /**
         * Like a work
         * @param { Number } workId 
         * @param { Boolean } unLike
         * @returns { Promise<Boolean> } successOrFailure
         */
        static like(workId, unLike) {
            return promise((r) => request[unLike ? "delete" : "post"](`${CodemaoApi.baseUrl}/nemo/v2/works/${workId}/like`, {headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(true)
                r(false)
            }))
        }
        /**
         * Collect a work
         * @param { Number } workId 
         * @param { Boolean } unCollect 
         * @returns { Promise<Boolean> } successOrFailure
         */
        static collect(workId, unCollect) {
            return promise((r) => request[unCollect ? "delete" : "post"](`${CodemaoApi.baseUrl}/nemo/v2/works/${workId}/collection`, {headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(true)
                r(false)
            }))
        }
        /**
         * Get the newest works
         * @param { Number } limit 
         * @param { Number } offset 
         * @returns { Promise<Object> } json
         */
        static getNewestWorks(limit, offset) {
            return promise((r) => request.get(`${CodemaoApi.baseUrl}/creation-tools/v1/pc/discover/newest-work?work_origin_type=ORIGINAL_WORK&offset=${offset ? offset : 0}&limit=${limit ? limit : 20}`, {headers: CodemaoApi.headers}, (err, res, body) => {
                if (res.statusCode >= 200 && res.statusCode < 300)
                    return r(stringToJson(body))
                r(null)
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
