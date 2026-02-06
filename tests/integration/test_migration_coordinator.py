# -*- coding: utf-8 -*-

"""
功能：迁移协调器的集成测试
"""

import unittest
from unittest.mock import Mock, MagicMock
from migration.migration_coordinator import MigrationCoordinator


class TestMigrationCoordinator(unittest.TestCase):
    """
    迁移协调器的集成测试
    """

    def setUp(self):
        """
        设置测试环境
        """
        # 创建虚拟机会话的模拟对象
        self.vm_session = Mock()
        self.vm_session.src_vm_name = "test-src-vm"
        self.vm_session.dst_vm_name = "test-dst-vm"
        self.vm_session.dst_vm_id = "vm-123"
        self.vm_session.dst_vm_image_id = "image-123"
        self.vm_session.update_detail_migrate_status = Mock()
        self.vm_session.export_dir = "/tmp/export"
        self.vm_session.upload_dir = "/tmp/upload"

        # 创建迁移协调器
        self.coordinator = MigrationCoordinator(self.vm_session)

        # 模拟各个步骤的成功执行
        self.coordinator.export_image.export = Mock(return_value=True)
        self.coordinator.deal_image.deal = Mock(return_value=True)
        self.coordinator.upload_image.upload = Mock(return_value=True)
        self.coordinator.create_vm.create = Mock(return_value=True)
        self.coordinator.create_vm.wait_for_vm_ready = Mock(return_value=True)
        self.coordinator.fix_tune.fix_and_tune = Mock(return_value=True)

    def test_migrate_success(self):
        """
        测试迁移成功的情况
        """
        result = self.coordinator.migrate()
        self.assertTrue(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_called_once()
        self.coordinator.create_vm.create.assert_called_once()
        self.coordinator.create_vm.wait_for_vm_ready.assert_called_once_with("vm-123")
        self.coordinator.fix_tune.fix_and_tune.assert_called_once()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_export_failure(self):
        """
        测试导出镜像失败的情况
        """
        self.coordinator.export_image.export = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_not_called()
        self.coordinator.upload_image.upload.assert_not_called()
        self.coordinator.create_vm.create.assert_not_called()
        self.coordinator.create_vm.wait_for_vm_ready.assert_not_called()
        self.coordinator.fix_tune.fix_and_tune.assert_not_called()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_deal_failure(self):
        """
        测试处理镜像失败的情况
        """
        self.coordinator.deal_image.deal = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_not_called()
        self.coordinator.create_vm.create.assert_not_called()
        self.coordinator.create_vm.wait_for_vm_ready.assert_not_called()
        self.coordinator.fix_tune.fix_and_tune.assert_not_called()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_upload_failure(self):
        """
        测试上传镜像失败的情况
        """
        self.coordinator.upload_image.upload = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_called_once()
        self.coordinator.create_vm.create.assert_not_called()
        self.coordinator.create_vm.wait_for_vm_ready.assert_not_called()
        self.coordinator.fix_tune.fix_and_tune.assert_not_called()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_create_failure(self):
        """
        测试创建虚拟机失败的情况
        """
        self.coordinator.create_vm.create = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_called_once()
        self.coordinator.create_vm.create.assert_called_once()
        self.coordinator.create_vm.wait_for_vm_ready.assert_not_called()
        self.coordinator.fix_tune.fix_and_tune.assert_not_called()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_wait_failure(self):
        """
        测试等待虚拟机就绪失败的情况
        """
        self.coordinator.create_vm.wait_for_vm_ready = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_called_once()
        self.coordinator.create_vm.create.assert_called_once()
        self.coordinator.create_vm.wait_for_vm_ready.assert_called_once_with("vm-123")
        self.coordinator.fix_tune.fix_and_tune.assert_not_called()
        self.vm_session.update_detail_migrate_status.assert_called()

    def test_migrate_fix_tune_failure(self):
        """
        测试修复调优失败的情况
        """
        self.coordinator.fix_tune.fix_and_tune = Mock(return_value=False)
        result = self.coordinator.migrate()
        self.assertFalse(result)
        self.coordinator.export_image.export.assert_called_once()
        self.coordinator.deal_image.deal.assert_called_once()
        self.coordinator.upload_image.upload.assert_called_once()
        self.coordinator.create_vm.create.assert_called_once()
        self.coordinator.create_vm.wait_for_vm_ready.assert_called_once_with("vm-123")
        self.coordinator.fix_tune.fix_and_tune.assert_called_once()
        self.vm_session.update_detail_migrate_status.assert_called()


if __name__ == "__main__":
    unittest.main()
