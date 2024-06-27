
# 如何使用环境登录 (Env Login)

如需使用环境登录，请先准备好您的账号和密码

## 使用.env文件

1. 在Aumiao-ts目录下创建一个名为".env"的文件
2. 在里面填入
   - ```CODEMAO_USERNAME="<YOUR USERNAME>"```<br/>```CODEMAO_PASSWORD="<YOUR PASSWORD>"```
   - 你需要修改其中两个变量
3. 运行login指令并且使用env登录
4. 如果提示没有找到env文件，可以使用--env参数来手动指定文件  
   例如： `node ./dist/index.js login --env "D:\.env"`

## 使用环境变量

### Windows >= 10

使用指令来设置环境变量

```bash
setx CODEMAO_USERNAME "<YOUR USERNAME>"
setx CODEMAO_PASSWORD "<YOUR PASSWORD>"
```
