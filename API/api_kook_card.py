import json

from API.api_kook import KOOKApi

sdk = KOOKApi()


class Card:
    def send_img(self, url: str, channel_id: int):
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
