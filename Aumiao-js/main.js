/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const { CodemaoApi } = require("./api")

function run(f) {
    return f()
}

CodemaoApi.setCookie("authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDb2RlbWFvIEF1dGgiLCJ1c2VyX3R5cGUiOiJzdHVkZW50IiwiZGV2aWNlX2lkIjowLCJ1c2VyX2lkIjoxMTc3MDc2OCwiaXNzIjoiQXV0aCBTZXJ2aWNlIiwicGlkIjoiNjVlZENUeWciLCJleHAiOjE3MjMyOTgxMTAsImlhdCI6MTcxOTQxMDExMCwianRpIjoiYzk2NDY5ZmUtZWNmZS00ZDA5LTkwM2MtMWE3NzgyNWFmMGZkIn0.3BK4JoOdUbIR8xAYLzaNSjca6wM1PrrAR8jHR7EUwCQ")

// TODO...

run(async () => console.log(await CodemaoApi.Work.like(227158550)))
