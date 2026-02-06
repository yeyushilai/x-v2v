#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志配置模块
"""

import logging
import os
import time

# 日志级别
LOG_LEVEL = logging.INFO

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, "v2v_migration_{}.log".format(time.strftime("%Y%m%d")))

# 配置日志
def setup_logger(name):
    """配置日志"""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 文件处理器
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)
    
    return logger

# 创建默认日志记录器
logger = setup_logger("v2v_migration")
