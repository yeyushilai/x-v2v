# -*- coding: utf-8 -*-

"""
通用工具
"""

import os
import hashlib


def get_file_size(file_path, unit="mb"):
    if unit == "mb":
        size = os.path.getsize(file_path) / float(1024 * 1024)
        # 确保返回值大于0
        return max(size, 0.01)
    else:
        # TODO:待开发
        raise


def find_file(file_path, file_name_list, fuzzy_search=False):

    compare_file_prefix_list = list()
    compare_file_format_list = list()
    if fuzzy_search:
        for file_name in file_name_list:
            compare_file_prefix, compare_file_format = file_name.split(".")
            compare_file_prefix_list.append(compare_file_prefix)
            compare_file_format_list.append(compare_file_format)

    for dir, folders, files in os.walk(file_path):
        for s_file in files:
            if "." not in s_file:
                continue
            if fuzzy_search:
                file_prefix, file_format = s_file.split(".")
                if (file_prefix in compare_file_prefix_list) and (
                        file_format in compare_file_format_list):
                    return True
            else:
                if s_file in file_name_list:
                    return True
    return False


def singleton(cls):
    _instance = {}
    global istc

    def _singleton(*args, **kargs):
        if cls not in _instance:
            istc = cls(*args, **kargs)
            _instance[cls] = istc
        return _instance[cls]

    return _singleton


def read_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content


def write_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)


def sha256_tool(content):
    sha = hashlib.sha256()
    sha.update(content)
    ret = sha.hexdigest()
    return ret


def FileLock(file_path):
    """
    文件锁类
    :param file_path: 文件路径
    """
    pass
