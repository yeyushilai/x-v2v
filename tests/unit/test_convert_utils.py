# -*- coding: utf-8 -*-

"""
功能：转换器工具模块的单元测试
"""

import unittest
import tempfile
import os
from utils.convert.convertorx import xml_file_to_json_file, xml_data_to_json_data


class TestConvertUtils(unittest.TestCase):
    """
    转换器工具模块的单元测试
    """

    def test_xml_data_to_json_data(self):
        """
        测试xml_data_to_json_data函数
        """
        test_xml = """
        <root>
            <name>test</name>
            <value>123</value>
        </root>
        """
        result = xml_data_to_json_data(test_xml)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["root"]["name"], "test")
        self.assertEqual(result["root"]["value"], "123")

    def test_xml_file_to_json_file(self):
        """
        测试xml_file_to_json_file函数
        """
        test_xml = """
        <root>
            <name>test</name>
            <value>123</value>
        </root>
        """

        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as xml_file:
            xml_file.write(test_xml)
            xml_file_path = xml_file.name

        json_file_path = xml_file_path.replace('.xml', '.json')

        try:
            # 测试函数
            result = xml_file_to_json_file(xml_file_path, json_file_path)
            self.assertIsInstance(result, dict)
            self.assertEqual(result["root"]["name"], "test")
            self.assertEqual(result["root"]["value"], "123")

            # 验证输出文件存在
            self.assertTrue(os.path.exists(json_file_path))
        finally:
            # 清理临时文件
            if os.path.exists(xml_file_path):
                os.unlink(xml_file_path)
            if os.path.exists(json_file_path):
                os.unlink(json_file_path)


if __name__ == "__main__":
    unittest.main()
