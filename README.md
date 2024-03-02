---
title: "CodeMao-AutoCommenter使用文档"
tags: [Auto,CodeMao]
categories: Python
index_img: /img/article/article_CodeMao_AutoCommer.jpg
date: 2023-11-06 12:00:00
comments: true
hide: false
---

{% note info %}
本文档更新于: 2024-01-25 凌晨
适用于Automatic-comments-v1.10版本
**本项目仅用于技术学习交流**
{% endnote %}

![signs](/img/article/article_CodeMao_AutoCommer_concent.jpg)

# 目录

- [项目简介](#项目简介)

- [作品说明](#作品说明)

- [功能列表](#功能列表)

- [使用教程](#使用教程)

- [功能详解](#功能详解)

- [项目总结](#项目总结)

- [下载地址](#下载地址)

## 项目简介

猫毡（雾）最强爬虫）

这个 Python 项目可以自动在编程猫网站上对作品进行**点赞**,**评论**以及**回复**,实现自动化模拟用户行为,以提高作品曝光率。✨

## 作品说明

原作:

- [python自动评论](https://shequ.codemao.cn/community/429585 )
- [Python评论自动回复](https://shequ.codemao.cn/community/430412)

**by** [伴雪纷飞](https://shequ.codemao.cn/user/2856172)

现作者账号转移至 [伴只狗头](https://shequ.codemao.cn/user/1888155714)

参考:

- 账号密码登录代码 **by** [PXstate](https://shequ.codemao.cn/user/1258391425) 
- 屏蔽词转换代码 **by** [伴雪纷飞](https://shequ.codemao.cn/user/2856172)

感谢《**A Byte of Python**》(《简明Python教程》)Swaroop C H撰 漠伦译 
- [说明文档](http://zhuanlan.zhihu.com/p/24672770)

为了讲解方便,文档中的{MAIN_FILEPATH}为您的爬虫所在目录,{FILEPATH}为结果记录文件所在目录

## 功能列表

- [x] 模拟登录
  - [x] 支持账号密码登录 🔐
  - [x] 支持直接 Cookie 登录 🍪
- [x] 获取最新作品
  - [x] 从网站接口获取最新上传作品列表 🆕
- [x] 获取最新回复
  - [x] 获取新的评论与回复以及点赞信息😉
- [x] 自动点赞
  - [x] 调用接口对作品点赞 👍
  - [x] 统计点赞次数 🔢
- [x] 自动评论
  - [x] 随机获取评论内容 💬
  - [x] 随机选择表情 😃
  - [x] 统计评论次数 📊
- [x] 自动回复
  - [x] 多种回复模式📃
- [x] 数据过滤
  - [x] 跳过已评论过的作品 ❌
  - [x] 跳过点赞数过多的作品 🙅‍♂️
- [x] 结果记录
  - [x] 记录已评论过的作品,避免重复 🙅‍
  - [x] 支持自定义保存位置和文件名
- [x] 随机间隔
  - [x] 每次操作后随机等待一定时间间隔 ⏳
- [x] 配置文件
  - [x] 支持修改评论回复内容✍
- [x] 侦测评论
  - [x] 侦测作品前300个评论,避免因为配置文件丢失而重复评论🎫
- [x] 速度至上
  - [x] 1.10版本全面重写🔍
  - [x] 优秀的代码逻辑💎
- [x] 生成文件内容优化🚀

## 使用教程

- **如果您使用的是以`.exe`结尾的可执行文件版本,可省略配置python,安装所需库以及运行文件这几步**

### 配置Python

访问如下网址`https://www.python.org/downloads/`

选择合适的**python**版本(3.9及以上,建议为最新)

- tips: 不会安装可以去看这篇文章[Python安装教程](https://zhuanlan.zhihu.com/p/632097212)

### 安装所需库

- requests
- ~~beautifulsoup4~~

可以使用 pip 直接安装:

```python
pip install requests
~~pip install beautifulsoup4~~
```

如果安装速度慢,可以先配置pip国内镜像源加速安装:

```python
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple # 永久设置
```
```python
pip install example -i https://pypi.tuna.tsinghua.edu.cn/simple # 暂时设置 
```

配置完成后,再使用pip安装库。

还有其他国内源,可以将`https://pypi.tuna.tsinghua.edu.cn/simple`替换

- [清华](https://pypi.tuna.tsinghua.edu.cn/simple)
- [阿里云](http://mirrors.aliyun.com/pypi/simple/)
- [中国科技大学](https://pypi.mirrors.ustc.edu.cn/simple/)
- [华中理工大学](http://pypi.hustunique.com/)
- [山东理工大学](http://pypi.sdutlinux.org/)
- [豆瓣](http://pypi.douban.com/simple/)

### 运行文件

使用Python自带的idle或其他IDE打开

按照指引运行

- tips: cookies具有时效性,配置文件并未保存,因此每次需要重新输入新的cookies

cookies获取教程(以edge浏览器为例)

- 访问如下网址`https://shequ.codemao.cn/`

- 输入账号密码,确保您已经登录

- 按下`F12`键,(笔记本电脑为`Fn`+`F12`),打开浏览器开发者工具

- 转到网络一栏,点击记录网络日志按钮

- 刷新网页,在网络日志中找到`details`打开

- 在标头中的请求表头中找到`Cookie`一项,右键复制,粘贴到爬虫中

### 文件结构

如果您已经运行过了一遍爬虫,爬虫将会生成三个文件:

```markdown
- Automatic-comments-v1.x.x.py    主程序文件 💻       位于{MAIN_FILEPATH}
- config.json  					  信息配置文件 📄     位于{MAIN_FILEPATH}
- example.txt     				  结果记录文件 📄     位于{FILEPATH}
```

### 自定义配置

请打开{MAIN_FILEPATH}中的config.json

如若您看到是的仅一行代码,请访问`https://www.bejson.com/explore/index_new/`或其他json格式化网站,将文件内容全部复制并格式化后覆盖掉原文本

现在,您看到的在该文件中,有两个大的字典:

- `Account`
- `Data`

`Account`存储的是您的账号信息,不可轻易更改

`Data`存储的是爬虫的输出数据:

- `proxies_list`存储了代理服务器地址,该功能还未正式投入使用
- `UNDO_LIST`存储了跳过的训练师编号,如若您想让爬虫跳过评论某人的作品,可以在此更改
- `comments`存储了发送的评论列表,爬虫会随机选取一个进行发送,您可以在此更改评论内容
- `emojis`存储了发送的表情列表,不可轻易更改
- `answers`存储了发送的回复列表,爬虫会随机选取一个进行发送,您可以在此更改回复内容

### 编译

如若您想让爬虫文件经过编译成为可执行文件

可使用如下库

- Nuitka
- Pyinstaller

现仅对Nuitka进行教学(Windows系统)

```python
pip install nuitka
```
在{MAIN_FILEPATH}目录,Shift+右键,在菜单中选择命令窗口并打开

也可以这样: win徽标键+r打开**运行**,输入cmd,在cmd中输入{MAIN_FILEPATH}目录所在盘符+半角冒号(例如`E:`),之后输入

`cd {MAIN_FILEPATH}`

在cmd中输入

`nuitka --standalone  --plugin-enable=upx  --show-progress --remove-output --windows-icon-from-ico=my.ico  --output-dir=out Automatic-comments-v1.10.0.py`

等待运行完成,即可在{MAIN_FILEPATH}下的out目录使用可执行文件版

## 功能详解

### 初始化账户信息
```python
Account = {
    "phonenum": " ", "password": " ", "filepath": " ",
    "userid": " ", "nickname": " ",
}
CONFIG_FILE_PATH = path.join(getcwd(), "config.json")
HEADERS = {...}
```
🔑 初始化账户信息,包括电话号码、密码、文件路径、用户ID和昵称。还定义了配置文件的路径和HTTP请求头。
### 预设数据类 `Pre_Data`
```python
class Pre_Data:
    def __init__(self):
        self.proxies_list = [{"http": "http://114.114.114.114:2333"}]
        self.contents = ["666＃°Д°", "加油！:O", ...]
        self.emojis = ["编程猫_666", "编程猫_棒", ...]
        self.answers = ["这是{}的自动回复...", "{}的自动回复来喽", ...]
```
📌 存储了预设的代理列表、评论内容、表情和自动回复模板。这些数据用于构建社区互动。
### 实际使用的数据类 `Data`
```python
class Data:
    def __init__(self):
        self.proxies_list = ([" "],)
        self.UNDO_LIST = [""]
        self.contents = ([" "],)
        self.emojis = ([" "],)
        self.answers = [" "]
```
📊 此类用于实际运行时存储和更新数据,如代理列表、评论内容等。
### 发送请求的函数 `send_request`
```python
def send_request(url, method, data=None, headers=HEADERS, direct=None):
    ...
```
🌐 此函数负责向指定的URL发送GET或POST请求。它还处理代理选择和异常情况。
### 检查配置文件是否存在的函数 `has_config_file`
```python
def has_config_file():
    ...
```
📁 检查配置文件是否存在,以确定是否需要加载或创建新的配置。
### 保存和加载账户信息的函数
```python
def save_account(path):
    ...
def load_account():
    ...
```
💾 这两个函数用于在配置文件中保存和加载账户信息及预设数据。
### 为账户信息提供交互式输入的函数 `input_account`
```python
def input_account():
    ...
```
👤 提供交互式界面以输入账户信息,如电话号码和密码。
### 登录函数 `login`
```python
def login():
    ...
```
🔐 处理用户登录逻辑,包括从网页解析所需的PID、发送登录请求、处理登录响应和更新账户信息。
### 检查评论的函数 `checkcomments`
```python
def checkcomments(work_id, special_id):
    ...
```
🔍 此函数用于检查特定作品的评论是否已存在。它通过发送请求到编程猫社区API,获取特定作品的评论数据,并遍历这些评论以检查是否包含特定用户ID的评论。
### 将文本写入指定文件的函数 `write`
```python
def write(text, name):
    ...
```
✍️ 用于将文本内容写入指定的文件。这主要用于记录已经进行过互动的作品ID,以避免重复互动。
### 排序文件中的数字的函数 `sort_numbers_in_file`
```python
def sort_numbers_in_file(input_file_path):
    ...
```
🔢 用于对文件中的数字进行排序。这通常用于优化生成的文件内容,例如将作品ID按照数值顺序排列。
### 点赞函数 `like_work`
```python
def like_work(cookie, work_id):
    ...
```
👍 对指定作品进行点赞。该函数发送POST请求到编程猫社区API,完成点赞操作,并处理响应以确认操作是否成功。
### 评论函数 `comment_work`
```python
def comment_work(cookie, work_id):
    ...
```
💬 对指定作品进行评论。它随机选择预设的评论内容和表情,然后发送POST请求进行评论。
### 回复函数 `reply_work`
```python
def reply_work():
    ...
```
🔄 处理接收到的回复消息。该函数首先检查是否有新的回复消息,然后根据消息类型（如评论回复或作品回复）发送适当的回复内容。
### 主函数 `main`
```python
def main():
    ...
```
🚀 定义了脚本的主要运行逻辑。它包括登录逻辑、用户交互以选择操作模式（如仅点赞、仅评论等）,并循环执行所选操作。

## 项目总结

这个项目主要运用了 requests、BeautifulSoup 等库模拟登录并解析页面,通过调用官方 API 实现自动化点赞和评论。✨

程序加入了一定的过滤机制,间隔设置以及代理来规避风控。🛡️

可以作为 Python 网络爬虫和接口调用的练手项目,与此同时需要注意合理使用,遵守网站规则。❗️

**如果有任何问题欢迎反馈,本项目仅用于技术学习交流。💬**

## 下载地址

- [GitHub访问加速](https://cloud.tsinghua.edu.cn/d/df482a15afb64dfeaff8/)
- [GitHub下载加速](https://ghproxy.com/) 
- [123云盘](https://www.123pan.com/s/oRHZVv-PBKtv.html)    提取码:*ygyc* 
- [蓝奏云网盘](https://zybqw.lanzout.com/b04e5pmcd)    密码:*ygyc* 
- **解压密码**:***zybqw***

## 联系我

如果您对此项目有任何问题或建议,欢迎随时联系我。😊

- 博客: zybqw.github.io
- 邮箱: zybqw@qq.com 📧
- 猫站主页: https://shequ.codemao.cn/user/12770114 🌐
- QQ: 3611198191
- 微信: Aurorzex

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zybqw/CodeMao-AutoCommenter&type=Date)](https://star-history.com/#zybqw/CodeMao-AutoCommenter&Date)


## 感谢您的阅读！😉
