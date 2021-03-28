import nonebot
from .config import Config
from nonebot.plugin import on_message, on_command
from nonebot.rule import to_me, Rule
from nonebot.typing import T_State
from nonebot.adapters.mirai import Bot, Event, message

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

#定义默认回复规则
def dafult_checker(bot: Bot, event: Event, state: T_State) -> bool:
    event_raw = event.normalize_dict()
    if event_raw['type'] == 'FriendMessage':
        return True
    if event_raw['type'] == 'GroupMessage':
        MessageChain = event_raw['message_chain']
        for Chain in MessageChain:
            if Chain['type'] == 'At' and Chain['target'] == 2832089175:
                return True
    return False

manual = on_message(rule=dafult_checker, priority=99)
help = on_command('help', priority=98)

@manual.handle()
async def manual_handle(bot: Bot, event: Event, state: T_State):
    await manual.finish(plugin_config.about)

@help.handle()
async def help_handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args == "r":
        await help.finish(plugin_config.help_r)
    elif args == "check":
        await help.finish(plugin_config.help_check)
    elif args == "choose":
        await help.finish(plugin_config.help_choose)
    elif args == "daily":
        await help.finish(plugin_config.help_daily)
    else:
        await help.finish(plugin_config.help)
