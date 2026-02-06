# -*- coding: utf-8 -*-

"""
功能：命令行工具模块的单元测试
"""

import unittest
from utils.cli.exec import normal_exec, bash_exec


class TestCliUtils(unittest.TestCase):
    """
    命令行工具模块的单元测试
    """

    def test_normal_exec(self):
        """
        测试normal_exec函数
        """
        returncode, stdout, stderr = normal_exec("echo 'Hello, world!'", timeout=5)
        self.assertEqual(returncode, 0)
        self.assertIn(b"Hello, world!", stdout)

    def test_bash_exec(self):
        """
        测试bash_exec函数
        """
        # 在Windows环境下，使用cmd.exe执行命令
        import os
        if os.name == 'nt':
            test_cmd = "echo Hello from cmd!"
            returncode, stdout, stderr = normal_exec(test_cmd, timeout=5)
            self.assertEqual(returncode, 0)
            self.assertIn(b"Hello from cmd!", stdout)
        else:
            test_cmd = "echo 'Hello from bash!'"
            returncode, stdout, stderr = bash_exec(test_cmd, timeout=5)
            self.assertEqual(returncode, 0)
            self.assertIn(b"Hello from bash!", stdout)


if __name__ == "__main__":
    unittest.main()
