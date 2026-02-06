# -*- coding: utf-8 -*-

"""
功能：迁移协调器
"""

from logger import logger
from migration.export.export_image import ExportImage
from migration.upload.upload_image import UploadImage
from migration.deal_image.deal_image import DealImage
from migration.create_vm.create_vm import CreateVM
from migration.fix_tune.fix_tune import FixTune
from constants.common import (
    MigrateStatus,
    MigratePattern
)


class MigrationCoordinator:
    """
    迁移协调器类
    """

    def __init__(self, vm_session):
        self.vm_session = vm_session
        self.export_image = ExportImage(vm_session)
        self.upload_image = UploadImage(vm_session)
        self.deal_image = DealImage(vm_session)
        self.create_vm = CreateVM(vm_session)
        self.fix_tune = FixTune(vm_session)

    def migrate(self):
        """
        执行完整的迁移流程
        """
        logger.info("Starting migration for VM: {vm_name}".format(
            vm_name=self.vm_session.src_vm_name
        ))

        try:
            # 1. 导出镜像
            if not self.export_image.export():
                self._handle_failure("Export image failed")
                return False

            # 2. 处理镜像
            if not self.deal_image.deal():
                self._handle_failure("Deal image failed")
                return False

            # 3. 上传镜像
            if not self.upload_image.upload():
                self._handle_failure("Upload image failed")
                return False

            # 4. 创建虚拟机
            if not self.create_vm.create():
                self._handle_failure("Create VM failed")
                return False

            # 5. 等待虚拟机就绪
            if not self.create_vm.wait_for_vm_ready(self.vm_session.dst_vm_id):
                self._handle_failure("Wait for VM ready failed")
                return False

            # 6. 修复调优
            if not self.fix_tune.fix_and_tune():
                self._handle_failure("Fix and tune failed")
                return False

            # 迁移成功
            self._handle_success()
            logger.info("Migration completed successfully for VM: {vm_name}".format(
                vm_name=self.vm_session.src_vm_name
            ))
            return True
        except Exception as e:
            logger.error("Migration failed with exception: {reason}".format(reason=str(e)))
            self._handle_failure(str(e))
            return False

    def _handle_success(self):
        """
        处理迁移成功的情况
        """
        self.vm_session.update_detail_migrate_status({
            "status": MigrateStatus.COMPLETED.value
        })

    def _handle_failure(self, reason):
        """
        处理迁移失败的情况
        """
        self.vm_session.update_detail_migrate_status({
            "status": MigrateStatus.FAILED.value,
            "err_msg": reason
        })


class ExportImageMigration(MigrationCoordinator):
    """
    导出镜像迁移类
    """
    pass


class UploadImageMigration(MigrationCoordinator):
    """
    上传镜像迁移类
    """
    pass
