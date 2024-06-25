## 目录

- [项目简介](#项目简介)

- [作品说明](#作品说明)

- [功能列表](#功能列表)

- [使用教程](#使用教程)

## 项目简介

猫毡（雾）最强爬虫）

这个 Python 项目可以自动在编程猫网站上实现自动化行为,以提高作品曝光率.✨

## 作品说明

原作:

- [python 自动评论](https://shequ.codemao.cn/community/429585)
- [Python 评论自动回复](https://shequ.codemao.cn/community/430412)
- [屏蔽词转换代码](https://shequ.codemao.cn/user/2856172)

**by** [伴雪纷飞](https://shequ.codemao.cn/user/2856172)

现作者账号转移至 [伴只狗头](https://shequ.codemao.cn/user/1888155714)

为讲解方便,文档中的{FILEPATH}为您的爬虫所在目录

## 功能列表

{% fold info @功能 %}

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

{% endfold %}

## 使用教程

- **如果您使用的是以`.exe`结尾的可执行文件版本,可省略配置 python,安装所需库以及运行文件这几步**

### 配置 Python

访问如下网址`https://www.python.org/downloads/`

选择合适的**python**版本(3.9 及以上,建议为最新)

- tips: 不会安装可以去看这篇文章[Python 安装教程](https://zhuanlan.zhihu.com/p/632097212)

### 安装所需库

- tips: 代码已内置自动安装功能,可跳过这一步骤

{% fold info @手动安装 %}

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

{% endfold %}

### 运行文件

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

### 文件结构

如果您已经运行过了一遍爬虫,爬虫将会生成三个文件:

```markdown
-   Aumiao.py 主程序文件 💻 位于{FILEPATH}
-   config.json 信息配置文件 📄 位于{FILEPATH}
```

### 自定义配置

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

### 编译

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

**如果有任何问题欢迎反馈,本项目仅用于技术学习交流.💬**

## 联系我

如果您对此项目有任何问题或建议,欢迎随时联系我.😊

- 博客: zybqw.github.io
- 邮箱: <zybqw@qq.com> 📧
- 猫站主页: <https://shequ.codemao.cn/user/12770114> 🌐
- QQ: 3611198191
- 微信: Aurorzex

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zybqw/Aumiao&type=Date)](https://star-history.com/#zybqw/Aumiao&Date)

## 感谢您的阅读！😉
