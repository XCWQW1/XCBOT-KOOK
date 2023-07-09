import json

from API.api_kook import KOOKApi

sdk = KOOKApi()


class Card:
    def send_img(self, url: str, channel_id: int) -> str:
        json_img = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": [
                    {
                        "type": "container",
                        "elements": [
                            {
                                "type": "image",
                                "src": url
                            }
                        ]
                    }
                ]
            }
        ]

        return sdk.send_channel_msg(json.dumps(json_img), 10, channel_id)

    def send_msg(self, msg: str, channel_id: int) -> str:
        json_data = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain-text",
                            "content": msg
                        }
                    }
                ]
            }
        ]

        return sdk.send_channel_msg(json.dumps(json_data), 10, channel_id)
