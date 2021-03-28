import nonebot
from .config import Config
from .RandGen import RandGen
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.mirai import Bot, Event

import random
import string
import re

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

dice = on_command('r', priority=2)
check = on_command('check', priority=2)

@dice.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["dice"] = args  # 如果用户发送了参数则直接赋值


@dice.got("dice", prompt="请输入掷骰表达式！输入/help r查看用法")
async def handle_dice(bot: Bot, event: Event, state: T_State):
    state["dice"] = state["dice"].replace(' ', '')
    if re.match('^\d+(?:d\d+(?:(?:\(|\[)\d+(?:\)|\]))?)?(?:\+\d+(?:d\d+(?:(?:\(|\[)\d+(?:\)|\]))?)?)*$', state["dice"]) == None:
        await dice.reject("输入的掷骰表达式格式错误！请重新输入！")
    rand_gen = RandGen()
    rand_gen.string_process(state["dice"])
    await dice.finish(rand_gen.msg_out)

@check.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["check"] = args  # 如果用户发送了参数则直接赋值

@check.got("check", prompt="请输入检定数值！输入/help check查看用法")
async def hanle_check(bot: Bot, event: Event, state: T_State):
    if re.match('^\d{1,3}(?:(?:\(|\[)\d+(?:\)|\]))?(?:\s.*)?$', state["check"]) == None:
        await check.reject("输入的数值格式错误！请重新输入！")
    rand_gen = RandGen()
    rand_gen.check_process(state["check"])
    await check.finish(rand_gen.msg_out)
