from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    about: str = '''Yuuki-bot
Powered By: Nonebot and Mirai
Created By: SinonJZH
All Rights Reserved.
输入/help查看帮助'''

    help: str = '''目前支持的指令
-----通用-----
/help (指令)： 显示这个页面，或指定指令的帮助
-----骰子-----
/r [掷骰表达式] ：投掷骰子，支持加法，支持惩罚/奖励骰
/c [检定数值] (鉴定属性) ：对某一属性进行检定，支持惩罚/奖励骰'''

    help_r: str = '''用法：/r [掷骰表达式]
投掷骰子，支持加法，支持惩罚/奖励骰，
如 1d100 , 3+1d10 等。
如需投掷惩罚骰，则在要投的数值后用括号表示惩罚骰的个数，
如 1d100(2) 表示附加两个惩罚骰。
如需投掷奖励骰，则在要投的数值后用中括号表示奖励骰的个数，
如 1d100[2] 表示附加两个奖励骰。
注：惩罚骰为高位多掷指定数量的骰子，取最大值，奖励骰则相反。'''

    help_c: str = '''用法：/c [检定数值] (鉴定属性)

'''

    class Config:
        extra = "ignore"
