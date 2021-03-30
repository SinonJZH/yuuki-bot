from pydantic import BaseSettings
import nonebot

class Config(BaseSettings):

    # plugin custom config
    enable: bool = True

    class Config:
        extra = "ignore"
