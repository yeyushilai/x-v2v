#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import xmltodict

from yaml import load, dump
from yaml import Loader, Dumper
from typing import Any, Optional, Union


class ConvertTool:

    @classmethod
    def xml_file_to_json_file(cls, xml_file: str, json_file: str) -> Optional[dict[str, Any]]:
        """ 将xml格式文件转为json格式文件（python对象） """
        with open(xml_file, mode="r") as f, open(json_file, "w") as f1:
            order_dict = xmltodict.parse(f.read(), encoding="utf-8")
            common_dict = json.loads(json.dumps(order_dict, ensure_ascii=False))
            json_str = json.dumps(common_dict)
            f1.write(json_str)
            return common_dict

    @classmethod
    def xml_data_to_json_data(cls, xml_data: str) -> dict[str, Any]:
        """ 将xml格式数据转为json格式数据 """
        order_dict = xmltodict.parse(xml_data, encoding="utf-8")
        return json.loads(json.dumps(order_dict, ensure_ascii=False))

    @classmethod
    def yaml_dump(cls, obj: Any) -> Optional[str]:
        """ 将json格式数据（python对象）转换为yaml格式数据 """

        try:
            output = dump(obj, Dumper=Dumper)
        except Exception as e:
            output = None
            print("dump yaml failed: %s" % e)
        return output

    @classmethod
    def yaml_load(cls, stream: str) -> Optional[Any]:
        """ 将yaml格式数据转换为json格式数据（python对象） """

        try:
            obj = load(stream, Loader=Loader)
        except Exception as e:
            obj = None
            print("load yaml failed: %s" % e)
        return obj

    @classmethod
    def float_to_int(cls, value: Union[float, int, str]) -> int:
        try:
            int_value = int(value)
        except Exception as e:
            int_value = int(float(value))
        return int_value

    @classmethod
    def dict_to_obj(cls, raw_dict: dict[str, Any]) -> Any:
        """ 字典转对象 """
        class Dict(dict):
            __setattr__ = dict.__setitem__
            __getattr__ = dict.__getitem__

        if not isinstance(raw_dict, dict):
            return raw_dict

        dt_obj = Dict()
        for k, v in raw_dict.items():
            dt_obj[k] = cls.dict_to_obj(v)
        return dt_obj

    @classmethod
    def obj_to_dict(cls, dict_obj: Any) -> dict[str, Any]:
        """ 对象转字典
            方法待确认
        """
        return dict_obj.__dict__


if __name__ == '__main__':
    dt_obj = ConvertTool.dict_to_obj({"name": "xxx", "age": 18})
    print(dir(dt_obj))
    print(type(dt_obj))
    print(dt_obj.name)
    print(dt_obj.age)
