import requests

from loguru import logger
from API.api_message import at_user
from API.api_iirose import APIIirose  # 大部分接口都在这里
from globals.globals import GlobalVal  # 一些全局变量 now_room_id 是机器人当前所在的房间标识，websocket是ws链接，请勿更改其他参数防止出bug，也不要去监听ws，websockets库只允许一个接收流
from API.api_get_config import get_master_id  # 用于获取配置文件中主人的唯一标识
from API.decorator.command import on_command, MessageType  # 注册指令装饰器和消息类型Enmu

API = APIIirose()  # 吧class定义到变量就不会要求输入self了（虽然我都带了装饰器没有要self的 直接用APIIirose也不是不可以 习惯了

weatherapi = "https://api.52vmy.cn/api/query/tian/three?city="


@on_command('>天气 ', True, command_type=[MessageType.room_chat, MessageType.private_chat])  # command_type 参数可让本指令在哪些地方生效，发送弹幕需验证手机号，每天20条。本参数需要输入列表，默认不输入的情况下只对房间消息做出反应，单个类型也需要是列表
async def weather(Message, text):  # 请保证同一个插件内不要有两个相同的指令函数名进行注册，否则只会保留最后一个注册的
    response = requests.get(weatherapi+text).json()
    await API.send_msg(Message, f'以下是{response["data"]["city"]}的天气：\n'
                           f'昨日-{response["data"]["data"][0]["Time"]}\n'
                           f'温度：{response["data"]["data"][0]["temperature"]}\n'
                           f'天气：{response["data"]["data"][0]["weather"]}\n'
                           f'风力：{response["data"]["data"][0]["bearing"]}\n'
                           f'空气质量：{response["data"]["data"][0]["air_quality"]}\n'
                           '\n'
                           f'今日-{response["data"]["data"][1]["Time"]}\n'
                           f'温度：{response["data"]["data"][1]["temperature"]}\n'
                           f'天气：{response["data"]["data"][1]["weather"]}\n'
                           f'风力：{response["data"]["data"][1]["bearing"]}\n'
                           f'空气质量：{response["data"]["data"][1]["air_quality"]}\n'
                           '\n'
                           f'明日-{response["data"]["data"][2]["Time"]}\n'
                           f'温度：{response["data"]["data"][2]["temperature"]}\n'
                           f'天气：{response["data"]["data"][2]["weather"]}\n'
                           f'风力：{response["data"]["data"][2]["bearing"]}\n'
                           f'空气质量：{response["data"]["data"][2]["air_quality"]}\n')