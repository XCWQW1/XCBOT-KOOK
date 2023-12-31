import inspect
import queue
import sys

import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Process, Queue


def start_thread(func, args):
    from API.api_log import Log

    # 创建一个队列对象
    result_queue = queue.Queue()

    # 在新线程中执行函数，并将结果存入队列中
    def thread_func():
        try:
            thread_result = func(*args)
            result_queue.put(thread_result)
        except Exception as e_1:
            Log.error("error", f"线程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
            result_queue.put(e_1)

    try:
        # 创建线程池
        with ThreadPoolExecutor() as executor:
            # 提交线程任务到线程池，并获取Future对象
            future = executor.submit(thread_func)

        # 等待线程执行完成，并获取结果
        future.result()

    except Exception as e:
        Log.error("error", f"多线程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
        return None

    # 获取所有线程的结果
    results = []
    for _ in as_completed([future]):
        results.append(result_queue.get())

    # 处理结果
    for result in results:
        # 如果结果是异常对象，将异常信息打印出来
        if isinstance(result, Exception):
            now_time_and_day = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
            log_file = f'errors/{now_time_and_day}.log'  # 日志文件名
            with open(log_file, 'a') as f_log:
                # 使用 traceback 模块打印完整的错误信息
                trace = ''.join(traceback.format_exception(type(result), result, result.__traceback__))
                # 设置日志内容
                logs = f"[{Log.now_time()}] [错误] [线] {inspect.getsourcefile(func)} | {traceback.print_exc()}"
                # 显示日志
                print(logs)
                f_log.write(f"子线程执行出错: {inspect.getsourcefile(func)} | {traceback.print_exc()}\n")
            return None

    # 返回结果
    return results[0]


def start_thread_no_return(func, args):
    from API.api_log import Log

    # 创建一个队列对象
    result_queue = queue.Queue()

    # 在新线程中执行函数，并将结果存入队列中
    def thread_func():
        try:
            thread_result = func(*args)
            result_queue.put(thread_result)
        except Exception as e_1:
            Log.error('error', f"多线程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
            result_queue.put(e_1)

    try:
        # 创建线程池
        with ThreadPoolExecutor() as executor:
            # 提交线程任务到线程池，并获取Future对象
            future = executor.submit(thread_func)

    except Exception as e:
        Log.error("error", f"多线程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
        return None

    # 获取所有线程的结果
    results = []
    for _ in as_completed([future]):
        results.append(result_queue.get())

    # 处理结果
    for result in results:
        # 如果结果是异常对象，将异常信息打印出来
        if isinstance(result, Exception):
            now_time_and_day = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
            log_file = f'errors/{now_time_and_day}.log'  # 日志文件名
            with open(log_file, 'a') as f_log:
                # 使用 traceback 模块打印完整的错误信息
                trace = ''.join(traceback.format_exception(type(result), result, result.__traceback__))
                # 设置日志内容
                logs = f"[{Log.now_time()}] [错误] [线] {inspect.getsourcefile(func)} | {traceback.print_exc()}"
                # 显示日志
                print(logs)
                f_log.write(f"子线程执行出错: {inspect.getsourcefile(func)} | {traceback.print_exc()}\n")


def start_process(func, args):
    from API.api_log import Log

    result_queue = Queue()

    def process_func():
        try:
            process_result = func(*args)
            result_queue.put(process_result)
        except Exception as e_1:
            # 打印完整的异常信息
            Log.error("error", f"多进程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
            result_queue.put(e_1)

    try:
        process = None
        if sys.platform == 'win32':
            # Windows平台
            from multiprocessing import freeze_support
            freeze_support()  # Windows下运行需要添加这行代码
            process = Process(target=process_func)

        else:
            # 其他平台
            process = Process(target=process_func)

        process.start()

    except Exception as e:
        Log.error("error", f"多进程报错：{inspect.getsourcefile(func)} | {traceback.print_exc()}")
        return None

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    for result in results:
        if isinstance(result, Exception):
            now_time_and_day = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
            log_file = f'errors/{now_time_and_day}.log'  # 日志文件名
            with open(log_file, 'a') as f_log:
                trace = ''.join(traceback.format_exception(type(result), result, result.__traceback__))
                logs = f"[{Log.now_time()}] [错误] [进] {inspect.getsourcefile(func)} | {str(result)}"
                print(logs)
                f_log.write(f"子进程执行出错: {inspect.getsourcefile(func)} | {str(trace)}\n")
