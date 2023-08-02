![signs](https://github.com/zybqw/CodeMao-AutoCommenter/assets/132246733/c5c7067d-3959-4da7-9ea5-3e571d8e6a57)

## 项目简介

这个 Python 项目可以自动在编程猫网站上对作品进行**点赞**,**评论**以及**回复**,实现自动化模拟用户行为,以提高作品曝光率。✨

## 作品说明

原作:

- [python自动评论](https://shequ.codemao.cn/community/429585 )
- [Python评论自动回复](https://shequ.codemao.cn/community/430412)

**by** [伴雪纷飞](https://shequ.codemao.cn/user/2856172)

现作者账号转移至 [伴只狗头](https://shequ.codemao.cn/user/1888155714)

参考:

- [PXstate](https://shequ.codemao.cn/user/1258391425) #制作了账号密码登录代码
- 屏蔽词转换代码 by [伴雪纷飞](https://shequ.codemao.cn/user/2856172)
- 以及广大cdn社区参考文档

Chat GPT,Claude 参与了代码修改!

感谢《A Byte of Python》(《简明Python教程》)Swaroop C H撰 漠伦译 [说明文档](http://zhuanlan.zhihu.com/p/24672770)

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
  - [x] 自定义评论内容与表情📗
  - [x] 随机获取评论内容 💬
  - [x] 随机选择表情 😃
  - [x] 统计评论次数 📊

- [x] 自动回复
  - [x] 多种回复模式📃
  - [x] 自定义回复内容📘

- [x] 数据过滤
  - [x] 跳过已评论过的作品 ❌
  - [x] 跳过点赞数过多的作品 🙅‍♂️
- [x] 结果记录
  - [x] 记录已评论过的作品,避免重复 🙅‍♀️
- [x] 随机间隔
  - [x] 每次操作后随机等待一定时间间隔 ⏳

- [x] 升级权限
  - [x] 自动升级脚本权限，方便读取🖋

- [ ] 异步处理
  - [ ] 正在学习**aiohttp**，**asyncio**库

## 环境需要

### 需要安装的库

- requests
- beautifulsoup4  
- configparser

### 库的安装方法

可以使用 pip 直接安装:

```python
pip install requests
pip install beautifulsoup4
```

如果使用pip安装速度慢,可以先配置pip国内镜像源加速安装:

- ```python
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple # 永久设置
  ```


- ```python
  pip install example -i https://pypi.tuna.tsinghua.edu.cn/simple # 暂时设置 
  ```

配置完成后,再使用pip安装库。

还有其他国内源

- [清华](https://pypi.tuna.tsinghua.edu.cn/simple)
- [阿里云](http://mirrors.aliyun.com/pypi/simple/)
- [中国科技大学](https://pypi.mirrors.ustc.edu.cn/simple/)
- [华中理工大学](http://pypi.hustunique.com/)
- [山东理工大学](http://pypi.sdutlinux.org/)
- [豆瓣](http://pypi.douban.com/simple/)

如果有其他更好的安装建议,也欢迎提出,我会继续完善。

## 文件结构

```
├── main.py 		主程序文件 💻
├── config.ini 	信息配置文件 📄
└── qwq.txt 		结果记录文件 📄
```

## 使用方法

1. 配置 Python 环境,安装需要的库 👩‍💻
2. 运行 Automatic-comments.py ▶️
3. 根据提示选择登录方式
   - 选择账号密码登录,输入编程猫账号和密码 👤
   - 选择 Cookie 登录,输入获取的 Cookie 值 🍪
4. 输入结果记录文件保存路径 📁
5. 选择仅**点赞**或**点赞+评论**或**点赞+评论+回复**✅
6. 程序将自动运行,打开作品列表并处理 🤖

## 主要功能详解

### 1. 模拟登录

​	支持账号密码登录和 Cookie 登录两种方式。

​	账号密码登录会调用登录接口,在登录成功后获取 Cookie 值保存。👤

​	Cookie 登录直接使用用户输入的 Cookie。🍪

​	登录成功后会保存账号信息,用于后续请求。🔑

​	(由于cookie具有时效性,并未保存)

### 2. 获取最新作品

​	使用官方接口获取最新上传的作品列表,作为处理对象。

​		`https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?limit={num1}&offset={num2}`🆕

​	其中`offset`表示忽略前**个作品，`limit`获取之后的作品列表

​		`{num1}`为必填项 # **num2  >=  5**

​		`{num2}`为选填项

### 3.获取最新回复

​	使用官方接口获取最新评论与回复,作为处理对象。

​		`https://api.codemao.cn/web/message-record/count`

​	如果有新回复，则获取最新列表

​		`https://api.codemao.cn/web/message-record?query_type=COMMENT_REPLY&limit={num1}&offset={num2}`

​		`{num1}`为必填项 # **num2  >=  5**

​		`{num2}`为选填项

### 4. 自动点赞

​	对每一个作品调用点赞接口进行点赞:

​		`https://api.codemao.cn/nemo/v2/works/{work_id}/like`  

​	如果点赞成功会打印日志,并统计成功点赞数。👍

​		`{work_id}`需获取最新作品，见响应体

### 5. 自动评论

​	从定义好的内容和表情列表中随机选择,构造评论数据,调用评论接口进行评论。

​		`https://api.codemao.cn/creation-tools/v1/works/{work_id}/comment`

​		`{work_id}`需获取最新作品，见响应体

​	如果评论成功会打印日志,并统计成功评论数，否则会打印错误码💬

### 6. 自动回复

​	从定义好的内容中随机选择,构造回复数据,调用回复接口进行评论。

- `https://api.codemao.cn/web/forums/replies/{replied_id}/comments`
  - 回复类型为WORK_COMMENT
  - `{replied_id}`需获取最新回复，见响应体			
- `https://api.codemao.cn/creation-tools/v1/works/{}/comment/{}/reply`
  - 回复类型为WORK_REPLY，WORK_REPLY_REPLY_FEEDBACK，WORK_REPLY_REPLY
  - `{business_id}`，`{replied_id}`需获取最新回复，见响应体	

​	如果回成功会打印日志,并统计成功回复数，否则会打印错误码💬

### 7.数据过滤

​	在评论前会校验该作品是否已被评论过,如果评论过则跳过。❌

​	同时也会判断作品点赞数,如果超过 50 则不评论。🙅‍♂️

### 8. 结果记录 

​	每次运行结束会保存当次的点赞数和评论数。📝

​	已评论过的作品编号会记录到文本文件中,避免重复评论。🙅‍♀️

### 9. 随机间隔

​	每个操作完成后会随机等待 12-16 秒左右时间,然后再处理下一个作品,避免请求过于频繁。⏳

## 项目总结

这个项目主要运用了 requests、BeautifulSoup 等库模拟登录并解析页面,通过调用官方 API 实现自动化点赞和评论。✨

程序加入了一定的过滤机制和间隔设置来规避风控。🛡️

可以作为 Python 网络爬虫和接口调用的练手项目,与此同时需要注意合理使用,遵守网站规则。❗️

**如果有任何问题欢迎反馈,本项目仅用于技术学习交流。💬**

## 下载地址

- [GitHub访问加速](https://cloud.tsinghua.edu.cn/d/df482a15afb64dfeaff8/)
- [GitHub下载加速](https://ghproxy.com/) 
- [123云盘](https://www.123pan.com/s/oRHZVv-PBKtv.html)    提取码:*ygyc* 
- [蓝奏云网盘](https://zybqw.lanzout.com/b04e5pmcd)    密码:*ygyc* 
- **解压密码**:***zybqw***

## 联系我

如果您对此项目有任何问题或建议，欢迎随时联系我。😊

- 邮箱：zybqw@qq.com 📧
- 个人主页：https://shequ.codemao.cn/user/12770114 🌐
  感谢您的阅读！😉
- QQ: 3611198191
- 微信: Aurorzex

## 我的Github 统计:

[![zybqw's GitHub stats](https://github-readme-stats.vercel.app/api?username=zybqw&show_icons=true&theme=vue)](https://github.com/zybqw)


