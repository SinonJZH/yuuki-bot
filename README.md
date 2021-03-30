<div align="center">
    <img src="yuuki.bmp" style="height:80px;border-radius:50%;">
</div>

# <center>yuuki-bot</center>
## <center>Sinon的yuki-botQQ机器人</center>
使用[Nonebot](https://v2.nonebot.dev/) & [Mirai](https://github.com/mamoe/mirai)框架运行  
正在绝赞开发中……

## 安装&配置
### 系统要求
1. Python 3.8+
2. JAVA 11+
3. Mysql
4. Redis
### 1.安装[Mirai](https://github.com/mamoe/mirai)
//
### 2.安装[Nonebot](https://v2.nonebot.dev/)
//
### 3.配置.env文件
将`.env.example`复制到创建的机器人的根目录，根据需要更名为`.env.{ENVIRONMENT}`  
`.env.example`文件各配置项说明：  
（其他配置项目请参考官方文档）
1. `MySQL_Address="127.0.0.1"`  MySQL地址
2. `MySQL_Port=3306`  MySQL端口,可省略，默认3306
3. `MySQL_DB=""`  MySQL数据库名称
4. `MySQL_User=""`  MySQL用户名
5. `MySQL_Pass=""`  MySQL密码
6. `Redis_Address="127.0.0.1"`  Redis地址
7. `Redis_Port=6379`  Redis端口,可省略，默认6379
8. `Redis_Prefix=""`  Redis键名前缀，可省略，默认为空
9. `Redis_DB=0`  Redis数据库，可省略，默认为0
## 指令
### 指令表
-----通用-----  
`/help (指令)`： 显示这个页面，或指定指令的帮助  
-----骰子-----  
`/r [掷骰表达式]` ：投掷骰子，支持加法，支持惩罚/奖励骰  
`/check [检定数值] (检定属性) `：对某一属性进行检定，支持惩罚/奖励骰  
`/choose [项目1] (项目2) (项目3) ...` ：从输入的项目中随机抽取一个  
`/daily` ： 测试今天的运气  
### 管理员指令
-----通用-----  
`/admin help (指令) `：显示这个帮助页面，或指定指令的帮助  
-----请求-----  
`/admin list `：显示待处理的请求列表  
`/admin approve [id] `：通过指定id的加群/好友请求  
`/admin reject [id] `：拒绝指定id的加群/好友请求  
`/admin detail [id] `：显示指定id请求的详细信息  
