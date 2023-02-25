import logging
import os
import datetime


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance = logging.getLogger()
            cls._instance.setLevel(logging.INFO)
            formatter = logging.Formatter("%(levelname)s %(asctime)s - %(message)s")
            current_time = datetime.datetime.now()
            dir_name = "Logs"

            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            file_handler = logging.FileHandler(dir_name + "\\Log_" + current_time.strftime("%Y-%m-%d") + ".log")
            stream_handler = logging.StreamHandler()
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            cls._instance.addHandler(file_handler)
            cls._instance.addHandler(stream_handler)

        return cls._instance

    @staticmethod
    def info(text):
        logger = Logger()
        logger.info(text)

    @staticmethod
    def warn(text):
        logger = Logger()
        logger.warning(text)

    @staticmethod
    def error(text):
        logger = Logger()
        logger.error(text)

    @staticmethod
    def start():
        logger = Logger()
        logger.info("=" * 20 + "NEW PROCESS" + "=" * 20)
        logger.info("Process has been started by : " + os.environ['USERNAME'])

    @staticmethod
    def finish():
        logger = Logger()
        logger.info("=" * 20 + "END PROCESS" + "=" * 20)