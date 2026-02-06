# -*- coding: utf-8 -*-

"""
功能：YAML工具函数
"""

import yaml


def yaml_load(file_obj):
    """
    加载YAML文件
    :param file_obj: 文件对象
    :return: YAML数据
    """
    return yaml.safe_load(file_obj)


def yaml_dump(data, file_obj):
    """
    保存数据到YAML文件
    :param data: 要保存的数据
    :param file_obj: 文件对象
    """
    yaml.safe_dump(data, file_obj, default_flow_style=False, allow_unicode=True)
