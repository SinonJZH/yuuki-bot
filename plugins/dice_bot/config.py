from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    daily_choice: list = [
        {
            "status" : "大吉",
            "msg"    : "今天似乎干什么事情都会顺利呢~"
        },
        {
            "status" : "吉",
            "msg"    : "有种做事会顺利的预感！"
        },
        {
            "status" : "小吉",
            "msg"    : "今天也是顺利的一天~"
        },
        {
            "status" : "凶",
            "msg"    : "今天做事还是小心为妙哦~"
        },
        {
            "status" : "大凶",
            "msg"    : "今天还是不要出门了吧……"
        }
    ]

    class Config:
        extra = "ignore"
