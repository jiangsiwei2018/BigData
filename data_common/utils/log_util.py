# coding=utf-8
import os
import traceback
import logging.config
import logging
import logging.handlers
from data_common.configure import constant
from data_common.configure.configure import Configure
from data_common.designs.singleton import SingletonType
from data_common.utils.file_util import FileUtil

KAFKA_MODE = False

class KeyedProducer:

    def __init__(self):
        pass

    def produce(self, msg):
        print(msg)


class KafkaLoggingHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.producer = KeyedProducer()

    def emit(self, record):
        # 忽略kafka的日志，以免导致无限递归。
        if 'kafka' in record.name:
            return
        try:
            # 格式化日志并指定编码为utf-8
            msg = self.format(record)
            # if isinstance(msg, str):
            #     msg = bytes(msg, encoding='utf-8')
            # kafka生产者，发送消息到broker。
            self.producer.produce(msg)

        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class LoggerUtil(metaclass=SingletonType):
    """
    Handler.setLevel()	设置handler将会处理的日志消息的最低严重级别
    Handler.setFormatter()	为handler设置一个格式器对象
    Handler.addFilter() 和 Handler.removeFilter()为handler添加 和 删除一个过滤器对象
    """
    def __init__(self):
        self.log_dir = self.get_logs_dir()
        self.log_file = self.log_dir + '/huge_data.log'
        # 创建logging handlers
        self.logger = logging.getLogger('huge-data')
        self.logger_level = Configure().get_config(constant.COMMON_DOMAIN,
                                                   constant.COMMON_LOGGER_LEVEL)
        self.logger.setLevel(self.logger_level)
        self.init_logger()

    def init_logger(self):
        logger_format = logging.Formatter(u'%(asctime)s-%(name)s-%(filename)s-'
                                          '[line:%(lineno)d]-%(levelname)s: %(message)s',
                                          datefmt='%a, %d %b %Y %H:%M:%S')
        if KAFKA_MODE:
            # 获取handler实例
            kafka_handler = KafkaLoggingHandler()
            # 添加handler
            kafka_handler.setFormatter(logger_format)
            self.logger.addHandler(kafka_handler)
        else:
            # 输出到文件
            file_handler = logging.handlers.\
                TimedRotatingFileHandler(self.log_file, when='M', interval=1, backupCount=5, encoding='utf-8')
            file_handler.setFormatter(logger_format)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logger_format)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    @staticmethod
    def get_logs_dir():
        _dir = os.path.dirname(__file__)
        logger_dir = os.path.split(
            os.path.split(_dir)[0])[0] + '/logs'
        if not FileUtil.exists(logger_dir):
            FileUtil.mk_dirs(logger_dir)
        return logger_dir


Logger = LoggerUtil().logger


def logger_exception():
    s = traceback.format_exc()
    for line in s.split('\n'):
        Logger.error(line)


if __name__ == '__main__':
    Logger.warning('dddddddddddddddddddd')
    Logger.error('dddddddddddddddddddd')
    Logger.debug('dddddddddddddddddddd')
    Logger.info('dddddddddddddddddddd')
    try:
        a = None
        b = 1
        a.eab()
    except:
        logger_exception()
