/*
 * Aumiao-js
 * 喵呜~
 * GitHub @满月叶
 */

const { CodemaoApi } = require("./api")

function run(f) {
    return f()
}

try {
    require("./test")()
} finally {}
