#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用日志管理
"""

import os
from typing import Callable, Final
from loguru import logger


def setup_logger():
    from core.config import config
    
    log_config = config.log
    log_dir = log_config.log_dir
    log_level = log_config.level
    backup_count = log_config.backup_count
    
    os.makedirs(log_dir, exist_ok=True)
    
    logger.remove()
    
    logger.add(
        os.path.join(log_dir, 'vmware-manager_{time}.log'),
        rotation='1 day',
        retention=f'{backup_count} days',
        compression='zip',
        level=log_level,
        enqueue=True,
        encoding='utf-8'
    )
    
    console_sink: Callable[[str], None] = lambda msg: print(msg, end="")
    logger.add(
        sink=console_sink,
        level='DEBUG',
        enqueue=True
    )


setup_logger()

__all__: Final[list[str]] = ['logger']

