import json

from API.api_kook import KOOKApi
from API.api_kook_card import Card

API = KOOKApi()
API_CARD = Card()


def plugin(msg_type, channel_id, channel_name, channel_message, channel_message_id, channel_user_id, channel_user_name,
           channel_user_nickname, channel_user_bot, target_id, target_name, data):
    # 基础指令触发以及发送
    if channel_message == "TEST-0":
        msg = 'TEST-0! Hello World!'  # 要发送的消息，此处为提升可读单独赋值给变量后发送，可以直接写到下方API的msg里
        API.send_channel_msg(msg, 1, channel_id,
                             channel_message_id)  # 发送消息, channel_message_id 可不提供，不提供则不引用触发消息直接发送, 1为消息类型 详见KOOK官方文档 发送卡片时需json.dumps(json_data)
        # API.send_channel_msg(msg, 1, channel_id)  # 不引用
        # API.send_channel_msg('TEST! Hello World!', 1, channel_id, channel_message_id)  # 直接写

    # 发送图片
    if channel_message == "TEST-1":
        file_url = API.upload_files('plugins/test.png')  # 先上传文件，可是文件路径，也可是文件的二进制
        API_CARD.send_img(file_url, channel_id)  # 发送

    # 发送自定义卡片
    if channel_message == "TEST-2":
        json_data = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": [
                    {
                        "type": "section",
                        "text": {
                            "type": "kmarkdown",
                            "content": "(font)自(font)[success](font)定(font)[purple](font)义(font)[warning](font)卡(font)[pink](font)片(font)[success]"
                        }
                    }
                ]
            }
        ]  # 可用kook官方的卡片编辑器生成json : https://www.kookapp.cn/tools/message-builder.html#/card
        API.send_channel_msg(json.dumps(json_data), 10, channel_id)  # 消息ID设置为10即可发送，引用无效

    # 对消息添加回应
    if channel_message == "TEST-3":
        API.add_reaction(channel_message_id, '✅')  # 要按顺序填入消息ID和要回应的emoji或emoji ID或GuilEmoji
