import json

import redis
import mysql.connector as mysql

import nonebot
from nonebot.adapters.mirai.event import Event, NewFriendRequestEvent, BotInvitedJoinGroupRequestEvent


class data_source:
    '为admin插件提供数据库接口'

    sql_connect = None
    redis_connect = None
    redis_prefix = None

    async def connect(self, mode=0):
        '''连接数据库
            参数mode：
            0：同时启用Mysql和redis连接
            1：仅启用redis连接
            2：仅启用Mysql连接
        '''
        global_config = nonebot.get_driver().config
        if mode == 0 or mode == 2:
            if global_config.mysql_port is None:
                global_config.mysql_port = 3306
            self.sql_connect = mysql.connect(
                host=global_config.mysql_address,
                user=global_config.mysql_user,
                passwd=global_config.mysql_pass,
                database=global_config.mysql_db,
                port=global_config.mysql_port
            )
        if mode == 0 or mode == 1:
            if global_config.redis_port is None:
                global_config.redis_port = 6379
            if global_config.redis_db is None:
                global_config.redis_db = 0
            if global_config.redis_pass is None:
                global_config.redis_pass = ""
            self.redis_connect = redis.StrictRedis(
                host=global_config.redis_adress,
                port=global_config.redis_port,
                db=global_config.redis_db,
                password=global_config.redis_pass,
                decode_responses=True
            )
            if global_config.redis_prefix:
                self.redis_prefix = global_config.redis_prefix + "_"
            else:
                self.redis_prefix = ""

    async def store_request(self, event: Event):
        '将请求事件存储至数据库'
        self.redis_connect.incr(self.redis_prefix + 'req_count')
        req_count = self.redis_connect.get(self.redis_prefix + 'req_count')
        event_dict = event.normalize_dict()
        event_id = event_dict['event_id']
        self.redis_connect.hset(
            self.redis_prefix + 'req_index', req_count, event_id)
        self.redis_connect.set(
            self.redis_prefix + 'req_event_' + str(event_id), json.dumps(event_dict))
        if isinstance(event, NewFriendRequestEvent):
            self.redis_connect.hset(self.redis_prefix + 'req_msg', req_count,
                                    str(req_count) + "：来自" + event_dict['nick'] + "的好友请求")
        else:
            self.redis_connect.hset(
                self.redis_prefix + 'req_msg', req_count, str(req_count) + "：加群邀请")
        return req_count

    async def get_request(self, request_id: int, normalize=False):
        '读取指定id的请求事件'
        event_id = self.redis_connect.hget(
            self.redis_prefix + 'req_index', request_id)
        if event_id is None:
            return None
        event_dict = json.loads(self.redis_connect.get(
            self.redis_prefix + 'req_event_' + str(event_id)))
        if normalize:
            return event_dict
        event_dict['eventId'] = event_dict['event_id']
        event_dict['fromId'] = event_dict['event_id']
        event_dict['groupId'] = event_dict['group_id']
        event = Event.new(event_dict)
        return event

    async def del_request(self, request_id: int):
        '删除指定id的请求事件'
        event_id = self.redis_connect.hget(
            self.redis_prefix + 'req_index', request_id)
        if event_id is None:
            return False
        self.redis_connect.delete(
            self.redis_prefix + 'req_event_' + str(event_id))
        self.redis_connect.hdel(self.redis_prefix + 'req_msg', request_id)
        self.redis_connect.hdel(self.redis_prefix + 'req_msg', request_id)
        return True

    async def request_list(self):
        '获取当前未处理的请求列表'
        req_list = ""
        req_list_raw = self.redis_connect.hvals(self.redis_prefix + 'req_msg')
        if req_list_raw is None:
            return None
        while len(req_list_raw) != 0:
            req_list += "\n" + req_list_raw.pop()
        return req_list
