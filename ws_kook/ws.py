import configparser
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

    # DEBUG
    # print(data)
    # DEBUG

    if data['s'] == 0 and data['d']['type'] == 9:
        try:
            channel_user_bot = data.get("d", "").get("extra", "").get("author", "").get("bot", "")
        except Exception as e:
            channel_user_bot = ""
        if not channel_user_bot:
            channel_type = data['d']['channel_type']
            if channel_type == "GROUP" and data['d']['type'] != 255:
                try:
                    channel_name = data.get("d", "").get("extra", "").get("channel_name", "")
                    channel_message = data.get("d", "").get("extra", "").get("kmarkdown", "").get("raw_content", "")
                    channel_user_id = data.get("d", "").get("extra", "").get("author", "").get("id", "")
                    channel_user_name = data.get("d", "").get("extra", "").get("author", "").get("username", "")
                    channel_user_nickname = data.get("d", "").get("extra", "").get("author", "").get("nickname", "")
                    target_id = data.get("d", "").get("extra", "").get("guild_id", "")
                except Exception as e:
                    channel_name = ""
                    channel_message = ""
                    channel_user_id = ""
                    channel_user_name = ""
                    channel_user_nickname = ""
                    target_id = ""
                channel_id = data.get("d", "").get("target_id", "")
                channel_message_id = data.get("d", "").get("msg_id", "")
                target_name = kook_api.get_target_name(target_id)
            else:
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
            if channel_type == "GROUP":
                Log.accepted_info(channel_message, channel_message_id, channel_user_nickname, channel_user_name,
                                  channel_user_id, channel_id, channel_name, target_id, target_name)

                for index, (plugin, name) in enumerate(zip(plugin_list, name_list)):
                    # 调用插件
                    try:
                        start_process(func=plugin, args=(channel_id, channel_name, channel_message, channel_message_id, channel_user_id, channel_user_name, channel_user_nickname, channel_user_bot, target_id, target_name, data))
                    except Exception as e:
                        Log.error("error", f"调用插件 {name} 报错：{e}")
    elif data['s'] == 0 and data['d']['type'] == 2:
        pass


async def connect_to_kook_server():
    retry_count = 5  # 最大重试次数
    retry_delay = 5  # 每次重试等待时间（秒）
    plugin_list, name_list = list_plugins()
    while retry_count > 0:
        try:
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

            kook_ws_url = get_ws(kook_token_type, kook_token)
            if kook_ws_url == '401':
                Log.error('error', '您的TOKEN无效，请检查机器人TOKEN是否正确')
                sys.exit(0)
            else:
                async with websockets.connect(kook_ws_url) as websocket:
                    async for message in websocket:
                        message = zlib.decompress(message)
                        data = json.loads(message)

                        if data['s'] == 1 and data['d']['code'] == 0:
                            Log.initialize(f'接收到了kook传回的HELLO包，判断为连接成功，获取到的会话ID为：{data["d"]["session_id"]}')
                        elif data['s'] == 1 and data['d']['code'] != 0:
                            Log.error('error', '没有接收到kook传回的HELLO包，判断为连接超时，请检查网络或是DNS服务等并重新尝试')
                            sys.exit(0)

                        # 使用新线程处理其他类型的消息
                        start_thread(process_message, (data, plugin_list, name_list))
        except Exception as e:
            Log.error('error', f"{e}")

