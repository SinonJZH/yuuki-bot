from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent

message_test = on_keyword({'是sb吗'}, rule=to_me(), priority=3)


@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await message_test.finish("是")
