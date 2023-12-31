import html
import os
import time

from colorama import init, Fore, Style

# 初始化colorama
init()


class LogSP:
    now_time_and_day_file = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

    @staticmethod
    def now_time():
        # 当前时间获取
        current_time = time.time()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
        return now_time

    @staticmethod
    def save_log(logs):
        log_sp = LogSP()
        if not os.path.exists('logs'):
            os.mkdir('logs')
        with open(f'logs/{LogSP.now_time_and_day_file}.log', 'a') as f_0:
            f_0.write(f"{logs}\n")

    @staticmethod
    def print_log(logs):
        print(logs)
        LogSP.save_log(logs)

    @staticmethod
    def initialize(initialize_txt):
        log_sp = LogSP()
        logs = f"[{log_sp.now_time()}] [初始] {initialize_txt}"
        print(logs)
        LogSP.save_log(logs)


class Log:
    @staticmethod
    def now_time():
        # 当前时间获取
        current_time = time.time()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
        return now_time

    @staticmethod
    def initialize(initialize_txt):
        logs = f"[{Log.now_time()}] [初始] {initialize_txt}"
        print(logs)
        LogSP.save_log(logs)

    @staticmethod
    def diy_log(log_type, log_content):
        logs = f"[{Log.now_time()}] [{log_type}] {log_content}"
        print(logs)
        LogSP.save_log(logs)

    # @是防止第一个变量输入为self
    # 正常信息
    @staticmethod
    def accepted_info(channel_type: str, msg_type: int, channel_message: str, channel_message_id: str, channel_user_nickname: str, channel_user_name: str, channel_user_id: int, channel_id: int, channel_name: str, target_id: int, target_name: str):
        if msg_type == 1:
            msg_type = '文字'
        elif msg_type == 2:
            msg_type = '图片'
        elif msg_type == 3:
            msg_type = '视频'
        elif msg_type == 4:
            msg_type = '文件'
        elif msg_type == 8:
            msg_type = '音频'
        elif msg_type == 9:
            msg_type = 'KMD'
        elif msg_type == 10:
            msg_type = '卡片'
        elif msg_type == 255:
            msg_type = '系统'
        else:
            msg_type = '其他'

        if msg_type != '系统':
            if channel_type == "GROUP":
                logs = f"[{Log.now_time()}] [信息] [频道] [接收] [{msg_type}] 服务器：[{target_name}({target_id})] 频道：[{channel_name}({channel_id})] [{channel_user_name}-{channel_user_nickname}({channel_user_id})] : {html.unescape(channel_message)} ({channel_message_id})"
            elif channel_type == "PERSON":
                logs = f"[{Log.now_time()}] [信息] [系统] [接收] [{msg_type}] 服务器：[{target_name}({target_id})] 频道：[{channel_name}({channel_id})] [{channel_user_name}-{channel_user_nickname}({channel_user_id})] : {html.unescape(channel_message)} ({channel_message_id})"
            elif channel_type == "BROADCAST":
                logs = f"[{Log.now_time()}] [信息] [系统] [接收] [{msg_type}] 服务器：[{target_name}({target_id})] 频道：[{channel_name}({channel_id})] [{channel_user_name}-{channel_user_nickname}({channel_user_id})] : {html.unescape(channel_message)} ({channel_message_id})"
            else:
                logs = None
        else:
            logs = None

        if logs:
            # 显示日志
            print(logs)
            LogSP.save_log(logs)

    # 发送 信息
    @staticmethod
    def send(send_type: int, send_msg: str, channel_id: int, channel_message_id: str):
        if send_type == 1:
            send_type = '文字'
        elif send_type == 2:
            send_type = '图片'
        elif send_type == 3:
            send_type = '视频'
        elif send_type == 4:
            send_type = '文件'
        elif send_type == 8:
            send_type = '音频'
        elif send_type == 9:
            send_type = 'KMD'
        elif send_type == 10:
            send_type = '卡片'
        elif send_type == 255:
            send_type = '系统'
        else:
            send_type = '其他'
        logs = f"[{Log.now_time()}] [信息] [发送] [{send_type}] {send_msg} ({channel_message_id}) -> 频道：{channel_id}"
        # 显示日志
        print(logs)
        LogSP.save_log(logs)

    # 错误信息
    @staticmethod
    def error(error_type: str, error_txt: str):
        if error_type == "channel":
            # 设置日志内容
            logs = Fore.RED + f"[{Log.now_time()}] [错误] [频道] {error_txt}" + Style.RESET_ALL
            # 显示日志
            print(logs)
            LogSP.save_log(logs)

        elif error_type == "error":
            # 设置日志内容
            logs = Fore.RED + f"[{Log.now_time()}] [错误] {error_txt}" + Style.RESET_ALL
            # 显示日志
            print(logs)
            LogSP.save_log(logs)
