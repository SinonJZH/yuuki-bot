from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    about: str = '''Yuuki-bot
Powered By: Nonebot & Mirai
Created By: SinonJZH
All Rights Reserved.
输入/help查看帮助'''

    help: str = '''目前支持的指令
-----通用-----
/help (指令)： 显示这个页面，或指定指令的帮助
-----骰子-----
/r [掷骰表达式] ：投掷骰子，支持加法，支持惩罚/奖励骰
/check [检定数值] (检定属性) ：对某一属性进行检定，支持惩罚/奖励骰
/choose [项目1] (项目2) (项目3) ... ：从输入的项目中随机抽取一个
/daily ：测试今天的运气'''

    help_r: str = '''用法：/r [掷骰表达式]
投掷骰子，支持加法，支持惩罚/奖励骰
如 1d100 , 3+1d10 等。
如需投掷惩罚骰，则在要投的数值后用括号表示惩罚骰的个数，
如 1d100(2) 表示附加两个惩罚骰。
如需投掷奖励骰，则在要投的数值后用中括号表示奖励骰的个数，
如 1d100[2] 表示附加两个奖励骰。
注：惩罚骰为高位多掷指定数量的骰子，取最大值，奖励骰则相反。'''

    help_check: str = '''用法：/check [检定数值] (检定属性)
更方便的数值检定指令，支持惩罚/奖励骰
检定数值为要检定的属性值（范围1~100），属性参数可选，为当前检定的属性
支持奖励，惩罚骰，语法格式和/r相同，
如/r 80(2) 理智   /r 50[2] 体力'''

    help_choose: str = '''用法：/choose [项目1] (项目2) (项目3) ...
用空格隔开每个项目，机器人会从中抽取一个。'''

    help_daily: str = '''用法：/daily
测试今天的运气。'''

    class Config:
        extra = "ignore"
