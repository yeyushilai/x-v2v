# -*- coding: utf-8 -*-

"""
功能：时间工具模块的单元测试
"""

import unittest
import time
from utils.time.timex import (
    now,
    now_local,
    now_local_format,
    get_format_datetime,
    now_local_timestamp,
    get_current_time
)


class TestTimeUtils(unittest.TestCase):
    """
    时间工具模块的单元测试
    """

    def test_now(self):
        """
        测试now函数
        """
        result = now()
        self.assertIsNotNone(result)

    def test_now_local(self):
        """
        测试now_local函数
        """
        result = now_local()
        self.assertIsNotNone(result)

    def test_now_local_format(self):
        """
        测试now_local_format函数
        """
        result = now_local_format()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_get_format_datetime(self):
        """
        测试get_format_datetime函数
        """
        from datetime import datetime
        test_datetime = datetime.now()
        result = get_format_datetime(test_datetime)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_now_local_timestamp(self):
        """
        测试now_local_timestamp函数
        """
        result = now_local_timestamp()
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_get_current_time(self):
        """
        测试get_current_time函数
        """
        result = get_current_time()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
