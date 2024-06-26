![Top Image](https://capsule-render.vercel.app/api?type=waving&color=66ccff&height=250&section=header)

![Typing SVG](https://readme-typing-svg.demolab.com?font=Hanalei+Fill&size=50&pause=1000&color=66CCFF&background=FFFFFF00&center=%E7%9C%9F&vCenter=%E7%9C%9F&repeat=%E7%9C%9F&random=%E5%81%87&width=200&height=100&lines=Aumiao)

# Aumiao

[![猫鱼a](https://img.shields.io/badge/猫鱼a-66ccff)](https://github.com/zybqw/)
[![Nomen](https://img.shields.io/badge/Nomen-66ccff)](https://github.com/helloyork/)
[![满月叶](https://img.shields.io/badge/满月叶-66ccff)](https://github.com/MoonLeeeaf/)
[![Python Badge](https://img.shields.io/badge/-Python-66ccff?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![Node.js Badge](https://img.shields.io/badge/-Node.js-66ccff?style=flat&logo=nodedotjs&logoColor=white)](https://nodejs.org/zh-cn)

## 这是什么

Aumiao是一款针对于编程猫社区的爬虫(划掉)

你说的对，但是《Aumiao》是一款由Aumiao开发团队开发的编程猫自动化工具
于2023年5月2日发布，工具以编程猫宇宙为舞台，玩家可以扮演扮演毛毡用户在这个答辩💩社区毛线🧶坍缩并邂逅各种不同的乐子人😋。在领悟了《猫站圣经》后，打败强敌扫厕所😡，在维护编程猫核邪铀删的局面的同时，逐步揭开编程猫社区的真相

官方网站（暂定）:<https://aurzex.top/article/Aumiao>

# 子项目

- **Aumiao-PY**
- **Aumiao-JS**

## Aumiao-JS

### 这是什么

Aumiao-JS是由**Nomen**开发的Aumiao子项目，用于支持NodeJS并且使用更强大的界面控制

### 这和Aumiao有什么区别

Aumiao-JS与Aumiao实现的功能基本一致

### 功能列表

- [ ] 身份验证
  - [ ] 单账号登录
    - [x] 本地凭据储存
    - [ ] Auth
      - [x] 凭据登录
      - [ ] Cookie登录
  - [ ] 多账号登录
    - [ ] 本地群组凭据管理
- [ ] 用户行为
  - [ ] 点赞作品
- [ ] 信息获取
  - [ ] 获取个人资料

### 如何使用

1. 安装NodeJS 18或以上
2. 运行`npm install -g typescript`
3. 将仓库克隆到本地
4. 运行`cd aumiao-js`
5. 运行`npm i`
6. 运行`npm run compile`
7. 运行`node ./dist/index.js --help`

### TODO

增加使用env文件的登录

## Aumiao-PY

### 作品说明

原作:

- [python 自动评论](https://shequ.codemao.cn/community/429585)
- [Python 评论自动回复](https://shequ.codemao.cn/community/430412)
- [屏蔽词转换代码](https://shequ.codemao.cn/user/2856172)

**by** [伴雪纷飞](https://shequ.codemao.cn/user/2856172)

现作者账号转移至 [伴只狗头](https://shequ.codemao.cn/user/1888155714)

为讲解方便,文档中的{FILEPATH}为您的爬虫所在目录

### 功能列表

- [x] 模拟登录 🔓
  - [x] 支持账号密码登录 🔐
  - [x] 支持直接 Cookie 登录 🍪
- [x] 自动点赞 👍
  - [x] 统计点赞次数 🔢
- [x] 自动评论 💬
  - [x] 自定义评论内容 📃
  - [x] 自定义表情 😃
  - [x] 统计评论次数 📊
- [x] 自动收藏 📌
  - [x] 收藏作者作品 🧡
- [x] 自动关注 🤝
  - [x] 关注作者 👀
- [x] 工作室常驻置顶 🏠
  - [x] 定时修改工作室简介 📝
- [x] 注册日期 📅
  - [x] 查看加入猫站时间 😃
- [x] 删除广告 💢
  - [x] 自动删除广告 💬
  - [x] 自定义关键词 📃
- [x] 信箱已读 📧
  - [x] 信箱全部已读 📊
- [x] 自动回复 🔄
  - [x] 自定义回复内容 📃
- [x] 获取随机昵称 🎉
  - [x] 调用接口获取
- [x] 获取粉丝列表 👥
  - [x] 粉丝列表导出
- [x] 数据过滤 🔁
  - [x] 跳过已评论过的作品 ❌
  - [x] 跳过点赞数过多的作品 🙅‍♂️
- [x] 随机间隔 ⏳
  - [x] 每次操作后随机等待一定时间间隔 ⏳
- [x] 配置文件 📑
  - [x] 支持修改信息 ✍

### 使用教程

- **如果您使用的是以`.exe`结尾的可执行文件版本,可省略配置 python,安装所需库以及运行文件这几步**

#### 配置 Python

访问如下网址`https://www.python.org/downloads/`

选择合适的**python**版本(3.9 及以上,建议为最新)

- tips: 不会安装可以去看这篇文章[Python 安装教程](https://zhuanlan.zhihu.com/p/632097212)

#### 安装所需库

- tips: 代码已内置自动安装功能,可跳过这一步骤

- requests

可以使用 pip 直接安装:

```python
pip install requests
```

如果安装速度慢,可以先配置 pip 国内镜像源加速安装:

```python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple # 永久设置
```

```python
pip install example -i https://pypi.tuna.tsinghua.edu.cn/simple # 暂时设置
```

配置完成后,再使用 pip 安装库.

还有其他国内源,可以将`https://pypi.tuna.tsinghua.edu.cn/simple`替换

- [清华](https://pypi.tuna.tsinghua.edu.cn/simple)
- [阿里云](http://mirrors.aliyun.com/pypi/simple/)
- [中国科技大学](https://pypi.mirrors.ustc.edu.cn/simple/)
- [华中理工大学](http://pypi.hustunique.com/)
- [山东理工大学](http://pypi.sdutlinux.org/)
- [豆瓣](http://pypi.douban.com/simple/)

#### 运行文件

使用 Python 自带的 idle 或其他 IDE 打开

按照指引运行

- tips: cookies 具有时效性,配置文件并未保存,因此每次需要重新输入新的 cookies

cookies 获取教程(以 edge 浏览器为例)

- 访问如下网址`https://shequ.codemao.cn/`

- 输入账号密码,确保您已经登录

- 按下`F12`键,(笔记本电脑为`Fn`+`F12`),打开浏览器开发者工具

- 转到网络一栏,点击记录网络日志按钮

- 刷新网页,在网络日志中找到`details`打开

- 在标头中的请求表头中找到`Cookie`一项,右键复制,粘贴到爬虫中

#### 文件结构

如果您已经运行过了一遍爬虫,爬虫将会生成三个文件:

```markdown
-   Aumiao.py 主程序文件 💻 位于{FILEPATH}
-   config.json 信息配置文件 📄 位于{FILEPATH}
```

#### 自定义配置

请打开{FILEPATH}中的 config.json

- tips: 如若您看到是的仅一行代码,请访问`https://www.bejson.com/explore/index_new/`或其他 json 格式化网站,将文件内容全部复制并格式化后覆盖掉原文本

现在,您看到的在该文件中,有两个字典:

- `Account`
- `Data`

`Account`存储的是您的账号信息,不可轻易更改

`Data`存储的是爬虫的输出数据:

- `blackroom`存储了跳过的训练师编号,如若您想让爬虫跳过评论某人的作品,可以在此更改
- `comments`存储了发送的评论列表,爬虫会随机选取一个进行发送,您可以在此更改评论内容
- `emojis`存储了发送的表情列表,请确保您已知晓编程猫社区内置的表情名称后再修改
- `answers`存储了发送的回复列表,爬虫会随机选取一个进行发送,您可以在此更改回复内容
- `ad`存储了广告的关键词,爬虫会根据关键词来筛选广告并删除,您可以在此更改关键词

#### 编译

如若您想让爬虫文件经过编译成为可执行文件

可使用如下库

- Nuitka
- Pyinstaller

现仅对 Nuitka 进行教学(Windows 系统)

```python
pip install nuitka
```

在{FILEPATH}目录,Shift+右键,在菜单中选择命令窗口并打开

也可以这样: win 徽标键+r 打开**运行**,输入 cmd,在 cmd 中输入{FILEPATH}目录所在盘符+半角冒号(例如`E:`),之后输入

`cd {FILEPATH}`

在 cmd 中输入

`nuitka --standalone --mingw64 --plugin-enable=upx --upx-binary="E:\zybqw\upx\upx.exe" --show-progress --show-memory --remove-output --windows-icon-from-ico=luo.ico --windows-company-name="猫鱼a" --windows-product-name="Aumiao" --windows-file-version="1.12.5" --windows-file-description="A CodeMao Community Tool" --output-dir=out Aumiao.py`

- tips: 如若没有 ico 文件,请删除`--windows-icon-from-ico=luo.ico`字段后再运行
- tips: 如果没有 upx 文件,请删除`--plugin-enable=upx --upx-binary="E:\zybqw\upx\upx.exe"`字段
    等待运行完成,即可在{FILEPATH}下的 out 目录使用可执行文件版

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zybqw/Aumiao&type=Date)](https://star-history.com/#zybqw/Aumiao&Date)

## 感谢您的阅读！😉
