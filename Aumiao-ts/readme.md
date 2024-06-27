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

1. 安装Node.js 18或以上从 [Nodejs.org](https://nodejs.org/)
2. 确保nodejs安装成功: `node --version && npm --version`
3. 克隆仓库: `git clone https://github.com/zybqw/Aumiao.git && cd ./Aumiao/Aumiao-ts`
4. 安装依赖: `node ./scripts/install.js`
5. 启动！`node ./dist/index.js`

### 一句话指令

```bash
git clone https://github.com/zybqw/Aumiao.git && cd ./Aumiao/Aumiao-ts && node ./scripts/install.js && node ./dist/index.js
```

## TODO

增加使用env文件的登录