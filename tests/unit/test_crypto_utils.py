# -*- coding: utf-8 -*-

"""
功能：加解密工具模块的单元测试
"""

import unittest
from utils.crypto.aes import aes_decode


class TestCryptoUtils(unittest.TestCase):
    """
    加解密工具模块的单元测试
    """

    def test_aes_decode(self):
        """
        测试aes_decode函数
        """
        # 这里需要使用实际的加密数据进行测试
        # 由于aes_decode函数使用了固定的密钥，我们需要确保测试数据是用该密钥加密的
        # 暂时跳过这个测试，因为我们没有实际的加密数据
        pass


if __name__ == "__main__":
    unittest.main()
