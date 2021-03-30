import string
import re

import nonebot
from nonebot.plugin import on_command, on_request
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.mirai import Bot, MessageSegment
from nonebot.adapters.mirai.event import Event, NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent

from .config import Config
from .data_source import data_source
from .help_text import HelpText

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


async def check_request(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, (NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent))


request = on_request(rule=check_request, priority=100)
admin = on_command("admin", priority=10, permission=SUPERUSER)


@admin.handle()
async def handle_admin_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["command"] = args  # 如果用户发送了参数则直接赋值
    else:
        state["command"] = "help"


@admin.got("command")
async def handle_admin(bot: Bot, event: Event, state: T_State):
    command = state["command"].split(" ")
    if command[0] == "help":
        if len(command) == 1:
            await admin.finish(HelpText.help)
        else:
            if command[1] == "approve":
                await admin.finish(HelpText.help_approve)
            elif command[1] == "reject":
                await admin.finish(HelpText.help_reject)
            elif command[1] == "list":
                await admin.finish(HelpText.help_list)
            else:
                await admin.finish(HelpText.help)
    elif command[0] == "approve":
        if len(command) == 1:
            await admin.finish("指令无效：需要指定请求id。")
        else:
            data = data_source()
            await data.connect(1)
            event_p = await data.get_request(int(command[1]))
            if event_p is None:
                await admin.finish("指令无效：没有指定id的请求")
                return
            await event_p.approve(bot)
            await data.del_request(int(command[1]))
            await admin.finish("接受了好友申请。")
    elif command[0] == "reject":
        if len(command) == 1:
            await admin.finish("指令无效：需要指定请求id。")
        else:
            data = data_source()
            await data.connect(1)
            event_p = await data.get_request(int(command[1]))
            if event_p is None:
                await admin.finish("指令无效：没有指定id的请求")
                return
            await event_p.reject(bot, 1)
            await data.del_request(int(command[1]))
            await admin.finish("拒绝了好友申请。")
    elif command[0] == "list":
        data = data_source()
        await data.connect(1)
        req_list = await data.request_list()
        if req_list is None:
            await admin.finish("当前没有未处理的请求。")
        else:
            req_list = "未处理请求列表：" + req_list
            await admin.finish(req_list)
    elif command[0] == "detail":
        if len(command) == 1:
            await admin.finish("指令无效：需要指定请求id。")
        else:
            data = data_source()
            await data.connect(1)
            event_dict = await data.get_request(int(command[1]), True)
            if event_dict is None:
                await admin.finish("指令无效：没有指定id的请求")
                return
            if(event_dict['type'] == "NewFriendRequestEvent"):
                message = "来自" + event_dict['nick'] + "（" + str(event_dict['from_id']) + \
                    ")的好友请求\n信息：" + event_dict['message']
            else:
                message = "来自（" + str(event_dict['from_id']) + \
                    "加入群" + str(event_dict['group_id']) + "的邀请。"
            message += "\n输入/admin approve " + command[1] + "通过" + \
                "\n或输入/admin reject " + command[1] + "拒绝"
            await admin.finish(message)


@request.handle()
async def handle_request(bot: Bot, event: Event, state: T_State):
    event_dict = event.normalize_dict()
    data = data_source()
    await data.connect(1)
    req_count = await data.store_request(event)
    message = ""
    if isinstance(event, NewFriendRequestEvent):
        message += "收到来自" + event_dict['nick'] + \
            "（" + str(event_dict['from_id']) + \
            "）的好友请求\n信息：" + event_dict['message']
    else:
        message += "收到加入群" + str(event_dict['group_id']) + "的邀请。"
    message += "\n输入/admin approve " + str(req_count) + "通过" + \
        "\n或输入/admin reject " + str(req_count) + "拒绝" + \
        "\n输入/admin detail " + str(req_count) + "再次查看此请求"
    superusers = global_config.superusers.copy()
    await bot.send_friend_message(superusers.pop(), [MessageSegment.plain(message)])
    await request.finish()
