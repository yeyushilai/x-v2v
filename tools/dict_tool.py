#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Union


class DictTool:

    @classmethod
    def fast_gen_dict(cls) -> dict[str, int]:
        """快速生成字典"""
        return dict(zip("abcd", range(4)))

    @classmethod
    def sum_dict(cls, dict_1: dict[Any, Union[int, float]], dict_2: dict[Any, Union[int, float]]) -> dict[Any, Union[int, float]]:
        """将两个字典合并，相同key的值相加，不同key值保留"""
        temp: dict[Any, Union[int, float]] = dict()
        for key in dict_1.keys() | dict_2.keys():
            temp[key] = sum([d.get(key, 0) for d in (dict_1, dict_2)])
        return temp
