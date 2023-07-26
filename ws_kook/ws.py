import asyncio
import configparser
import random
import time
import zlib
import json
import sys

import websockets
from API.api_find_plugin import list_plugins
from API.api_log import Log
from API.api_thread import start_process, start_thread
from API.api_kook import KOOKApi
from ws_kook.gateway import get_ws

#################################################
# 一个websocket客户端，用于连接kook的websocket服务器 #
#################################################


link_status = 1
sleep_time = 0
session_id = ''
sn = 1
wait_json = []


# 读取配置文件
def load_config() -> [str, str]:
    # 配置文件路径
    c_config_path = "config/config.ini"

    # 读取配置文件
    c_config = configparser.ConfigParser()
    c_config.read(c_config_path)

    # 获取相应的配置信息
    c_kook_token = c_config.get("kook", "token")
    c_kook_token_type = c_config.get("kook", "token_type")

    return c_kook_token, c_kook_token_type


# 用于连接ws后处理json和调用插件
def process_message(data, plugin_list, name_list):
    kook_token, kook_token_type = load_config()
    kook_api = KOOKApi()

    try:
        channel_user_bot = data.get("d", {}).get("extra", {}).get("author", {}).get("bot", "")
    except Exception as e:
        channel_user_bot = ""

    if not channel_user_bot:
        channel_type = data.get("d").get("channel_type", "")
        channel_extra = {}
        channel_name = ""
        channel_message = ""
        channel_user = {}
        channel_user_id = ""
        channel_user_name = ""
        channel_user_nickname = ""
        target_id = ""
        msg_type = ""

        try:
            channel_extra = data.get("d", {}).get("extra", {})
            channel_name = channel_extra.get("channel_name", "")
            msg_type = data.get("d", {}).get("type", "")
            if msg_type == 9:
                channel_message = data.get("d", "").get("extra", "").get("kmarkdown", "").get("raw_content", "")
            else:
                channel_message = data.get("d").get("content", "")
            channel_user = channel_extra.get("author", {})
            channel_user_id = channel_user.get("id", "")
            channel_user_name = channel_user.get("username", "")
            channel_user_nickname = channel_user.get("nickname", "")
            target_id = channel_extra.get("guild_id", "")

        except Exception as e:
            pass

        channel_id = data.get("d", {}).get("target_id", "")
        channel_message_id = data.get("d", {}).get("msg_id", "")
        target_name = kook_api.get_target_name(target_id)

    else:
        msg_type = ""
        channel_type = ""
        channel_id = ""
        channel_name = ""
        channel_message = ""
        channel_message_id = ""
        channel_user_id = ""
        channel_user_name = ""
        channel_user_nickname = ""
        channel_user_bot = ""
        target_id = ""
        target_name = ""

    Log.accepted_info(channel_type, msg_type, channel_message, channel_message_id, channel_user_nickname,
                      channel_user_name,
                      channel_user_id, channel_id, channel_name, target_id, target_name)

    for index, (plugin, name) in enumerate(zip(plugin_list, name_list)):
        # 调用插件
        try:
            start_process(func=plugin, args=(
                msg_type, channel_id, channel_name, channel_message, channel_message_id, channel_user_id,
                channel_user_name, channel_user_nickname, channel_user_bot, target_id, target_name, data))
        except Exception as e:
            Log.error("error", f"调用插件 {name} 报错：{e}")


async def connect_to_kook_server():
    global link_status
    global sleep_time
    global session_id
    global sn
    global wait_json
    retry_count = 5  # 最大重试次数
    retry_delay = 5  # 每次重试等待时间（秒）

    plugin_list, name_list = list_plugins()
    kook_token, kook_token_type = load_config()

    if kook_token_type == "None":
        Log.initialize('请选择鉴权方式：')
        Log.initialize('1，Bot')
        Log.initialize('2，Bearer')
        token_type = input('输入序号：')
        config_path = "config/config.ini"
        config = configparser.ConfigParser()

        if token_type == '1':
            token_type = 'Bot'
            config.read(config_path)
            config.set("kook", "token_type", token_type)
            with open(config_path, "w") as f:
                config.write(f)
            Log.initialize('已写入配置文件，日后更改请更改config/config.ini')

        elif token_type == '2':
            token_type = 'Bearer'
            config.read(config_path)
            config.set("kook", "token_type", token_type)
            with open(config_path, "w") as f:
                config.write(f)
            Log.initialize('已写入配置文件，日后更改请更改config/config.ini')

        elif not token_type in ['1', '2']:
            Log.error('error', '不支持除1和2以外的其他参数')
            sys.exit(0)
    else:
        kook_token, kook_token_type = load_config()

    async def add_sleep_time():
        global sleep_time
        if sleep_time != 60:
            sleep_time = sleep_time + 1

    while retry_count > 0:
        try:
            if link_status == 1:
                gateway = get_ws(kook_token_type, kook_token)
                if gateway['code'] == 0:
                    kook_ws_url = gateway['data']['url']
                    link_status = 2
                elif gateway["code"] == 401:
                    Log.error('error', '您的TOKEN无效，请检查机器人TOKEN是否正确')
                    sys.exit(0)
                else:
                    Log.error('error', f'访问Gateway失败，正在指数回退 {sleep_time}s 后将会重新获取Gateway')
                    time.sleep(sleep_time)
                    await add_sleep_time()
            elif link_status == 2:
                async def send_ping(websocket):
                    global sn
                    while True:
                        await websocket.send({"s": 2, "sn": sn})
                        await asyncio.sleep(random.randint(25, 35))  # 随机等待 30 -+5 秒后再发送心跳 ping 包

                async def receive_pong(websocket):
                    while True:
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=6)
                            print(response)
                        except asyncio.TimeoutError:
                            Log.error('error', 'ping 超时，进入指数回退')
                            await add_sleep_time()
                            break

                async with websockets.connect(kook_ws_url) as websocket:
                    async for message in websocket:
                        # DEBUG
                        # print(zlib.decompress(message))
                        # DEBUG

                        message = zlib.decompress(message)
                        data = json.loads(message)
                        if data['s'] == 1 and data['d']['code'] == 0:
                            link_status = 3
                            Log.initialize(
                                f'接收到了kook传回的HELLO包，判断为连接成功，获取到的会话ID为：{data["d"]["session_id"]}')
                            session_id = data["d"]["session_id"]

                            if sleep_time != 0:
                                sleep_time = 0
                                Log.diy_log('信息', 'ws连接成功！指数回退已重置为 0s')

                        elif data['s'] == 1 and data['d']['code'] == 40103:
                            Log.error('error',
                                      f'您的TOKEN已过期，正在指数回退 {sleep_time}s 后将会重新获取Gateway并连接ws')
                            time.sleep(sleep_time)
                            await add_sleep_time()

                        elif data['s'] == 1 and data['d']['code'] != 0:
                            link_status = 1
                            Log.error('error',
                                      f'没有接收到kook传回的HELLO包，判断为连接超时，请检查网络或是DNS服务，正在指数回退 {sleep_time}s 后将会重新获取Gateway并连接ws')
                            time.sleep(sleep_time)
                            await add_sleep_time()

                        if data['s'] == 0:
                            if sn == 65536:
                                sn = 1

                            if wait_json:
                                if sn + 1 == wait_json[0]['sn']:
                                    sn = wait_json[0]['sn']
                                    # 使用新线程处理其他类型的消息
                                    if link_status == 3:
                                        start_thread(process_message, (wait_json[0], plugin_list, name_list))
                                    del wait_json[0]

                            if sn == data['sn']:
                                sn = sn + 1
                                # 使用新线程处理其他类型的消息
                                if link_status == 3:
                                    start_thread(process_message, (data, plugin_list, name_list))
                            else:
                                if data['sn'] > sn:
                                    wait_json.append(data)

        except Exception as e:
            Log.error('error', f"{e}")
