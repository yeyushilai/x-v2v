# -*- coding: utf-8 -*-

"""
功能：通用工具模块的单元测试
"""

import unittest
import tempfile
import os
from utils.common.common import (
    get_file_size,
    find_file,
    singleton,
    read_file,
    write_file,
    sha256_tool
)


class TestCommonUtils(unittest.TestCase):
    """
    通用工具模块的单元测试
    """

    def test_get_file_size(self):
        """
        测试get_file_size函数
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            file_path = f.name

        try:
            size = get_file_size(file_path, unit="mb")
            self.assertIsInstance(size, float)
            self.assertGreater(size, 0)
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_find_file(self):
        """
        测试find_file函数
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试文件
            test_file_path = os.path.join(temp_dir, "test.txt")
            with open(test_file_path, "w") as f:
                f.write("test content")

            # 测试精确匹配
            self.assertTrue(find_file(temp_dir, ["test.txt"]))
            self.assertFalse(find_file(temp_dir, ["nonexistent.txt"]))

            # 测试模糊匹配
            self.assertTrue(find_file(temp_dir, ["test.txt"], fuzzy_search=True))
            self.assertFalse(find_file(temp_dir, ["nonexistent.txt"], fuzzy_search=True))

    def test_singleton(self):
        """
        测试singleton装饰器
        """
        @singleton
        class TestClass:
            def __init__(self, value):
                self.value = value

        instance1 = TestClass(1)
        instance2 = TestClass(2)
        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.value, 1)

    def test_read_file(self):
        """
        测试read_file函数
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            file_path = f.name

        try:
            content = read_file(file_path)
            self.assertEqual(content, 'test content')
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_write_file(self):
        """
        测试write_file函数
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            file_path = f.name

        try:
            write_file(file_path, 'test content')
            with open(file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, 'test content')
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_sha256_tool(self):
        """
        测试sha256_tool函数
        """
        content = b'test content'
        hash_value = sha256_tool(content)
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 64)


if __name__ == "__main__":
    unittest.main()
