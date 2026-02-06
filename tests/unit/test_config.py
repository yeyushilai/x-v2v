# -*- coding: utf-8 -*-

"""
功能：配置管理模块的单元测试
"""

import unittest
from config import Config, DEFAULT_CONFIG


class TestConfig(unittest.TestCase):
    """
    配置管理模块的单元测试
    """

    def test_init_with_default_config(self):
        """
        测试使用默认配置初始化
        """
        config = Config()
        self.assertEqual(config.get("common.max_migrating_num"), DEFAULT_CONFIG["common"]["max_migrating_num"])
        self.assertEqual(config.get("export_image.timeout"), DEFAULT_CONFIG["export_image"]["timeout"])

    def test_get_nonexistent_key(self):
        """
        测试获取不存在的配置键
        """
        config = Config()
        self.assertIsNone(config.get("nonexistent.key"))
        self.assertEqual(config.get("nonexistent.key", "default"), "default")

    def test_set_key(self):
        """
        测试设置配置键
        """
        config = Config()
        config.set("test.key", "value")
        self.assertEqual(config.get("test.key"), "value")

    def test_merge_config(self):
        """
        测试合并配置
        """
        config = Config(default_config={
            "common": {
                "key1": "value1",
                "key2": "value2"
            }
        })
        self.assertEqual(config.get("common.key1"), "value1")
        self.assertEqual(config.get("common.key2"), "value2")


if __name__ == "__main__":
    unittest.main()
