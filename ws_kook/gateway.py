import time

import requests

from API.api_log import Log


def get_ws(token_type, token) -> str:
    url = 'https://www.kookapp.cn/api/v3/gateway/index'

    headers = {
        "Authorization": f"{token_type} {token}"
    }

    response = requests.get(url, headers=headers).json()
    if response['code'] == 401:
        time.sleep(5)
        Log.error('error', '访问Gateway失败，五秒后尝试')
        return "401"
    else:
        return response['data']['url']
