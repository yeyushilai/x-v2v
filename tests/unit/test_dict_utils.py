# -*- coding: utf-8 -*-

"""
功能：字典工具模块的单元测试
"""

import unittest
from utils.dict.dict_tool import Dict, dict_to_obj


class TestDictUtils(unittest.TestCase):
    """
    字典工具模块的单元测试
    """

    def test_dict_class(self):
        """
        测试Dict类
        """
        d = Dict()
        d.key1 = "value1"
        self.assertEqual(d.key1, "value1")
        self.assertEqual(d["key1"], "value1")

        d["key2"] = "value2"
        self.assertEqual(d.key2, "value2")
        self.assertEqual(d["key2"], "value2")

    def test_dict_to_obj(self):
        """
        测试dict_to_obj函数
        """
        test_dict = {
            "key1": "value1",
            "key2": {
                "nested_key": "nested_value"
            }
        }
        obj = dict_to_obj(test_dict)
        self.assertEqual(obj.key1, "value1")
        self.assertEqual(obj.key2.nested_key, "nested_value")


if __name__ == "__main__":
    unittest.main()
