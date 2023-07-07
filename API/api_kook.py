import configparser
import json

from typing import Optional, Union

import requests

from API.api_log import Log

#######################################################################
#                                 接口                                 #
#                          用于调用kook的http api                       #
#                 如果访问失败将会返回json中的状态代码(code)的值             #
#######################################################################


# 加载配置文件
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


# 接口总类
class KOOKApi:
    # 初始化函数
    def __init__(self):
        self.token, self.token_type = load_config()  # 获取token和token_type
        self.koo_url = "https://www.kookapp.cn"  # kook的地址

    def kook_http_api_post(self, api_url, post_data) -> json:
        """
        带访问头post访问KOOK的API用于简化后面函数的一些操作
        :param api_url:  # 提交的API地址
        :param post_data:  # 提交的数据 json 格式
        :return:  # 访问后返回访问接口后返回的未经过任何处理的原始json
        """
        url = self.koo_url + api_url

        headers = {
            "Authorization": f"{self.token_type} {self.token}",
            "X-Rate-Limit-Limit": "5",
            "X-Rate-Limit-Remaining": "0",
            "X-Rate-Limit-Reset": "14",
            "X-Rate-Limit-Bucket": "user/info",
            "X-Rate-Limit-Global": ""
        }

        response = requests.post(url, headers=headers, data=post_data).json()  # 访问接口
        return response

    def kook_http_api_get(self, api_url, get_data) -> json:
        """
        带访问头get访问KOOK的API用于简化后面函数的一些操作
        :param api_url:  # 提交的API地址
        :param get_data:  # 提交的数据 json 格式
        :return:  # 访问后返回访问接口后返回的未经过任何处理的原始json
        """
        url = self.koo_url + api_url

        headers = {
            "Authorization": f"{self.token_type} {self.token}",
            "X-Rate-Limit-Limit": "5",
            "X-Rate-Limit-Remaining": "0",
            "X-Rate-Limit-Reset": "14",
            "X-Rate-Limit-Bucket": "user/info",
            "X-Rate-Limit-Global": ""
        }

        response = requests.get(url, headers=headers, params=get_data).json()
        return response

    def send_channel_msg(self, send_msg: str or json, msg_type: int, channel_id: int, quote: Optional[str] = None) -> str:
        """
        给指定频道发送指定消息
        :param quote:  # 要引用的消息ID，可以为空，空则不引用直接发送
        :param msg_type:  # 消息了类型，根据kook官方文档的那个走即可：https://developer.kookapp.cn/doc/http/message#%E5%8F%91%E9%80%81%E9%A2%91%E9%81%93%E8%81%8A%E5%A4%A9%E6%B6%88%E6%81%AF
        :param send_msg:  # 需要发送的消息
        :param channel_id:  # 要发送到频道的频道id
        :return:  # 成功后返回消息id
        """
        if quote is None:
            post_data = {
                "type": msg_type,
                "target_id": channel_id,
                "content": send_msg
            }
        else:
            post_data = {
                "type": msg_type,
                "target_id": channel_id,
                "content": send_msg,
                "quote": quote
            }

        request = self.kook_http_api_post("/api/v3/message/create", post_data)

        if request['code'] == 0:
            if msg_type == 1:
                Log.send(send_msg, channel_id, request['data']['msg_id'])
            else:
                Log.send("[非正常消息]", channel_id, request['data']['msg_id'])
            return request['data']['msg_id']
        else:
            return request['code']

    def get_target_name(self, target_id: int) -> str:
        """
        获取指定服务器的名称
        :param target_id:  # 服务器id
        :return:  # 成功后返回服务器名称
        """
        get_data = {
            "guild_id": target_id
        }
        request = self.kook_http_api_get("/api/v3/guild/view", get_data)
        if request['code'] == 0:
            return request['data']['name']
        else:
            return request['code']

    def upload_files(self, file_name: Union[str, bytes]) -> str:
        """
        上传文件
        :param file_name:  # 输入str类 则文件精准路径会自动转换为二进制，输入bytes会直接发送，方便图片渲染等直接发送二进制
        :return:  # 成功后返回文件直连
        """

        url = self.koo_url + "/api/v3/asset/create"

        payload = {}
        if type(file_name) == str:
            files = [
                ('file', ('file', open(file_name, 'rb'), 'image/png'))
            ]
        else:
            files = [
                ('file', ('file', file_name, 'image/png'))
            ]
        headers = {
            "Authorization": f"{self.token_type} {self.token}"
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload, files=files).json()
        except Exception as e:
            response = {'code': '1', 'data': {'url': 'error'}}

        if response['code'] == 0:
            return response['data']['url']
        else:
            return response['code']

    #################
    #     未完工     #
    #################

    def game(self, type: int) -> str:
        """
        未完工欢迎pr
        :param type:
        :return:
        """
        get_data = {
            "type": type
        }
        request = self.kook_http_api_get("/api/v3/game", get_data)
        print(request)
        if request['code'] == 0:
            return request['data']
        else:
            return request['code']

    def create_game(self, name: str) -> str:
        post_data = {
            "name": name
        }
        request = self.kook_http_api_post("/api/v3/game/create", post_data)
        print(request)
        if request['code'] == 0:
            return request['data']['id']
        else:
            return request['code']

    def activity_game(self, id: int, data_type: int) -> str:
        post_data = {
            "id": id,
            "data_type": data_type
        }
        request = self.kook_http_api_post("/api/v3/game/activity", post_data)
        return request['code']