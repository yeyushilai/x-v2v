# -*- coding: utf-8 -*-

"""
功能：异常处理模块的单元测试
"""

import unittest
from exceptions import (
    V2VMigrationError,
    ExportImageError,
    DealImageError,
    UploadImageError,
    CreateVMError,
    FixTuneError,
    handle_exception
)


class TestExceptions(unittest.TestCase):
    """
    异常处理模块的单元测试
    """

    def test_v2v_migration_error(self):
        """
        测试V2VMigrationError异常
        """
        with self.assertRaises(V2VMigrationError) as cm:
            raise V2VMigrationError("Test error")
        self.assertEqual(str(cm.exception), "Test error")

    def test_export_image_error(self):
        """
        测试ExportImageError异常
        """
        with self.assertRaises(ExportImageError) as cm:
            raise ExportImageError("Export error")
        self.assertEqual(str(cm.exception), "Export error")

    def test_deal_image_error(self):
        """
        测试DealImageError异常
        """
        with self.assertRaises(DealImageError) as cm:
            raise DealImageError("Deal error")
        self.assertEqual(str(cm.exception), "Deal error")

    def test_upload_image_error(self):
        """
        测试UploadImageError异常
        """
        with self.assertRaises(UploadImageError) as cm:
            raise UploadImageError("Upload error")
        self.assertEqual(str(cm.exception), "Upload error")

    def test_create_vm_error(self):
        """
        测试CreateVMError异常
        """
        with self.assertRaises(CreateVMError) as cm:
            raise CreateVMError("Create error")
        self.assertEqual(str(cm.exception), "Create error")

    def test_fix_tune_error(self):
        """
        测试FixTuneError异常
        """
        with self.assertRaises(FixTuneError) as cm:
            raise FixTuneError("Fix tune error")
        self.assertEqual(str(cm.exception), "Fix tune error")

    def test_handle_exception_decorator(self):
        """
        测试异常处理装饰器
        """
        @handle_exception
        def raise_exception():
            raise Exception("Test exception")

        with self.assertRaises(V2VMigrationError):
            raise_exception()

    def test_handle_exception_decorator_no_exception(self):
        """
        测试异常处理装饰器（无异常情况）
        """
        @handle_exception
        def no_exception():
            return "Success"

        result = no_exception()
        self.assertEqual(result, "Success")


if __name__ == "__main__":
    unittest.main()
