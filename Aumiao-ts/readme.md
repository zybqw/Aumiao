# Aumiao-ts

## 这是什么

Aumiao-ts 是由**Nomen**开发的 Aumiao 子项目，用于支持 Node.js 并且使用更强大的界面控制

## 这和 Aumiao-py 有什么区别

Aumiao-ts 与 Aumiao-py 实现的功能基本一致

## 这和 Aumiao-js 有什么区别

Aumiao-ts 使用 TypeScript 进行编写，并且使用了更加现代化的统一命令框架和界面

## 功能列表

- [ ] 身份验证
  - [x] 单账号登录
    - [x] 本地凭据储存
    - [x] Auth
      - [x] 凭据登录
      - [x] Cookie登录
  - [ ] 多账号登录
    - [ ] 本地群组凭据管理
- [ ] 用户行为
  - [ ] 点赞作品
- [ ] 信息获取
  - [ ] 获取个人资料

## 如何使用

1. 安装 Node.js 18 或以上
2. 运行 `npm install -g typescript` 下载编译工具
3. 将仓库克隆到本地
4. 在项目根目录中运行 `cd Aumiao-ts` 导航到子项目
5. 运行 `npm i` 下载所需的依赖
6. 运行 `npm run compile` 进行编译
7. 运行 `node ./dist/index.js --help` 并且享受

## TODO

增加使用env文件的登录