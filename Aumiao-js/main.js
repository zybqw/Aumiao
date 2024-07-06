/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const { CodemaoApi } = require("./api")

function run(f) {
    return f()
}


// TODO...

run(async () => console.log(await CodemaoApi.Work.like(227158550)))
