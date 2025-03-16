import logging
from logging.handlers import RotatingFileHandler
import sys

def configure_logger():
    # 创建根日志器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 通用日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 控制台Handler（所有级别）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # 文件Handler（DEBUG级别，自动轮转）
    file_handler = RotatingFileHandler(
        'game.log',
        maxBytes=1024*1024*5,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger