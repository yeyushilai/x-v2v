# -*- coding: utf-8 -*-

"""
字典工具
"""


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_obj(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    d = Dict()
    for k, v in dict_obj.items():
        d[k] = dict_to_obj(v)
    return d
