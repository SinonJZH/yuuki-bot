class HelpText:
    '储存帮助文本'

    help: str = '''管理员指令
-----通用-----
/admin help (指令) ：显示这个帮助页面，或指定指令的帮助
-----请求-----
/admin list ：显示待处理的请求列表
/admin approve [id] ：通过指定id的加群/好友请求
/admin reject [id] ：拒绝指定id的加群/好友请求
/admin detail [id] ：显示指定id请求的详细信息
'''

    help_approve: str = '''用法：/admin approve [id]
通过指定id的加群/好友请求
可使用/admin list查看待处理请求列表
'''

    help_reject: str = '''用法：/admin reject [id]
拒绝指定id的加群/好友请求
可使用/admin list查看待处理请求列表
'''

    help_list: str = '''用法：/admin list
显示待处理的请求列表
'''

    help_detail: str = '''用法：/admin detail [id]
显示指定id请求的详细信息
'''
