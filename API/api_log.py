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
    def accepted_info(channel_message, channel_message_id, channel_user_nickname, channel_user_name, channel_user_id, channel_id, channel_name, target_id, target_name):
        # 设置群日志内容
        logs = f"[{Log.now_time()}] [信息] [频道] [接收] 服务器：[{target_name}({target_id})] 频道：[{channel_name}({channel_id})] [{channel_user_name}-{channel_user_nickname}({channel_user_id})] : {html.unescape(channel_message)} ({channel_message_id})"
        # 显示日志
        print(logs)
        LogSP.save_log(logs)

    # 发送 信息
    @staticmethod
    def send(send_msg, channel_id, channel_message_id):
        # 设置日志内容
        logs = f"[{Log.now_time()}] [信息] [频道] [发送] {send_msg} ({channel_message_id}) -> 频道：{channel_id} "
        # 显示日志
        print(logs)
        LogSP.save_log(logs)

    # 错误信息
    @staticmethod
    def error(q_message_type, error_txt):
        if q_message_type == "group":
            # 设置日志内容
            logs = Fore.RED + f"[{Log.now_time()}] [错误] [频道] {error_txt}" + Style.RESET_ALL
            # 显示日志
            print(logs)
            LogSP.save_log(logs)

        elif q_message_type == "error":
            # 设置日志内容
            logs = Fore.RED + f"[{Log.now_time()}] [错误] {error_txt}" + Style.RESET_ALL
            # 显示日志
            print(logs)
            LogSP.save_log(logs)

    # 撤回 群信息
    @staticmethod
    def del_msg(q_message_type, q_user_id="", q_message_id="", q_group_name="", q_user_name=""):
        if q_message_type == "group":
            # 设置日志内容
            logs = f"[{Log.now_time()}] [信息] [群] [撤回] [{q_message_id}] ({q_message_id}) -> [{q_group_name}({q_user_id})] "
            # 显示日志
            print(logs)
            LogSP.save_log(logs)
        elif q_message_type == "private":
            # 设置日志内容
            logs = f"[{Log.now_time()}] [信息] [私] [撤回] [{q_message_id}] ({q_message_id}) -> [{q_user_name}({q_user_id})] "
            # 显示日志
            print(logs)
            LogSP.save_log(logs)
"""
    @staticmethod
    def accepted_group_add_request(q_add_flag, q_add_comment, q_add_group_id, q_add_user_id, q_add_user_nickname):
        # 设置群日志内容
        logs = f"[{Log.now_time()}] [信息] [加群] 群：[{QQApi.get_group(q_add_group_id)}({q_add_group_id})] 用户：[{q_add_user_nickname}({q_add_user_id})] 验证信息：{q_add_comment} flag：{q_add_flag}"
        # 显示日志
        print(logs)
        LogSP.save_log(logs)

    @staticmethod
    def group_leave(q_sub_type, q_group_member_group_id, q_group_member_user_id, q_group_member_user_nickname):
        if q_sub_type == "leave":
            # 设置群日志内容
            logs = f"[{Log.now_time()}] [信息] [退群] 群：[{QQApi.get_group(q_group_member_group_id)}({q_group_member_group_id})] 用户：[{q_group_member_user_nickname}({q_group_member_user_id})]"
            # 显示日志
            print(logs)
            LogSP.save_log(logs)

    @staticmethod
    def group_kick(q_sub_type, q_group_member_group_id, q_group_member_user_id, q_group_member_user_nickname, q_group_member_operator_id, q_group_member_operator_nickname):
        if q_sub_type == "kick":
            # 设置群日志内容
            logs = f"[{Log.now_time()}] [信息] [踢出] 群：[{QQApi.get_group(q_group_member_group_id)}({q_group_member_group_id})] 踢出用户：[{q_group_member_user_nickname}({q_group_member_user_id})] 操作用户：[{q_group_member_operator_nickname}({q_group_member_operator_id})]"
            # 显示日志
            print(logs)
            LogSP.save_log(logs)
"""