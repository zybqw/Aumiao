
const Tips: string[] = [
    "你知道吗，全局参数--no-sensei可以让面板停止叫你sensei（这真的很没用",
    "你知道吗，每次你修改完Aumiao-TS代码之后都要重新编译才能生效",
    "如果你不想创建env文件，也可以设置环境变量（Windows）",
    "如果你在启动脚本时遇到了问题，可以尝试使用node ./dist/index.js",
    "我很忙.jpg",
    "你知道吗，Aumiao-TS的代码是用TypeScript写的，与它的其他两个子项目不同，ts版本有着令人骄傲的界面和交互",
    "用node aumiao可以自动安装依赖",
    "你猜猜你要刷新几次才能看见这条tip？"
];
function tip() {
    return Tips[Math.floor(Math.random() * Tips.length)];
}

export {
    Tips,
    tip
}

