import logging
import inspect


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3

    logger = None
    level = INFO

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(threadName)s - %(message)s",
            handlers=[
                logging.StreamHandler()
            ])

        self.logger = logging.getLogger(__name__ + '.logger')

    @staticmethod
    def set_level(lvl):
        Logger.level = lvl

    @staticmethod
    def __get_call_info():
        stack = inspect.stack()

        # stack[1] gives previous function ('info' in our case)
        # stack[2] gives before previous function and so on

        fn = stack[2][1]
        ln = stack[2][2]
        func = stack[2][3]

        return fn, func, ln

    def error(self, message, *args):
        if Logger.level <= Logger.ERROR:
            message = "E {} - {} at line {}: {}".format(*self.__get_call_info(), message)
            self.logger.info(message, *args)

    def warn(self, message, *args):
        if Logger.level <= Logger.WARN:
            message = "W {} - {} at line {}: {}".format(*self.__get_call_info(), message)
            self.logger.info(message, *args)

    def info(self, message, *args):
        if Logger.level <= Logger.INFO:
            message = "I {} - {} at line {}: {}".format(*self.__get_call_info(), message)
            self.logger.info(message, *args)

    def debug(self, message, *args):
        if Logger.level <= Logger.DEBUG:
            message = "D {} - {} at line {}: {}".format(*self.__get_call_info(), message)
            self.logger.info(message, *args)
