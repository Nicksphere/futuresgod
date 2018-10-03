import time
import os
# from conf.path_config import log_dir
import logging.handlers

log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/futuresgod/logs"
# log
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# 日志输出的级别
log_level = logging.DEBUG
# 全局的日志格式设置
logging.basicConfig(level=log_level, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
# 定义一个KB_SERVICE日志记录器
log_all = logging.getLogger("AICHATBOT_SERVICE")

# 日志名
logNameByDay = log_dir + "/" + 'futuresgod'
# 创建一个handler，用于写入日志文件
fh = logging.handlers.TimedRotatingFileHandler(logNameByDay, when='MIDNIGHT', interval=1, backupCount=30, encoding='utf-8')
fh.suffix = "%Y-%m-%d.log"
# 设置文件记录器的输出级别
fh.setLevel(log_level)
# 定义日志输出格式
format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
fh.setFormatter(format)
# 将logger添加到handle里面
log_all.addHandler(fh)

#
# def custom_time(*args):
#     utc_dt = utc.localize(datetime.utcnow())
#     my_tz = timezone("Asia/Shanghai")
#     converted = utc_dt.astimezone(my_tz)
#     return converted.timetuple()
#
#
# logging.Formatter.converter = custom_time


def get_logger_root():
    return log_all


if __name__ == '__main__':
    Logger = get_logger_root()
    count = 1
    while True:
        count += 1
        time.sleep(1)
        # Logger.error(f'dsafasdfasf{count}')
        Logger.info('dsafasdfasf')
