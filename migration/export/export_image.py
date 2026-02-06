# -*- coding: utf-8 -*-

"""
功能：导出镜像模块
"""

import os
import time
from logger import logger
from utils.cli.exec import normal_exec, bash_exec
from utils.common.common import find_file
from constants.template import EXPORT_IMAGE_CMD_TEMPLATE
from constants.common import (
    EXPORT_IMAGE_TIMEOUT,
    EXPORT_IMAGE_MAX_RETRY_TIMES,
    EXPORT_IMAGE_CMD_VI_PREFIX,
    EXPORT_IMAGE_DEFAULT_PARAMS,
    EXPORT_IMAGE_DST_FORMAT_OVA,
    RunningDetailMigrateStatus
)
from exceptions import ExportImageError, handle_migration_exception


class ExportImage:
    """
    导出镜像类
    """

    def __init__(self, vm_session):
        self.vm_session = vm_session

    def export(self):
        """
        导出镜像
        """
        @handle_migration_exception(self.vm_session)
        def _export():
            logger.info("Starting to export image for VM: {vm_name}".format(
                vm_name=self.vm_session.src_vm_name
            ))

            # 更新状态为导出中
            self.vm_session.update_detail_migrate_status({
                "running_detail_status": RunningDetailMigrateStatus.EXPORT_IMAGE.value
            })

            # 构建导出命令
            export_cmd = self._build_export_cmd()
            logger.info("Export command: {cmd}".format(cmd=export_cmd))

            # 执行导出命令
            returncode, stdout, stderr = normal_exec(
                export_cmd, timeout=EXPORT_IMAGE_TIMEOUT
            )
            if returncode != 0:
                raise ExportImageError("Export image failed: {stderr}".format(stderr=stderr))

            logger.info("Image exported successfully")
            return True

        return _export()

    def _build_export_cmd(self):
        """
        构建导出命令
        """
        # 构建导出命令的参数
        export_params = EXPORT_IMAGE_DEFAULT_PARAMS.copy()
        export_params.update({
            "src_vm_id": self.vm_session.src_vm_id,
            "dst_format": EXPORT_IMAGE_DST_FORMAT_OVA,
            "dst_path": self.vm_session.export_dir
        })

        # 构建导出命令
        export_cmd = EXPORT_IMAGE_CMD_TEMPLATE.format(**export_params)
        if EXPORT_IMAGE_CMD_VI_PREFIX:
            export_cmd = "{prefix} {cmd}".format(
                prefix=EXPORT_IMAGE_CMD_VI_PREFIX, cmd=export_cmd
            )

        return export_cmd

    def find_exported_image(self):
        """
        查找导出的镜像文件
        """
        ova_files = ["*.ova"]
        if find_file(self.vm_session.export_dir, ova_files, fuzzy_search=True):
            logger.info("Found exported OVA file")
            return True
        return False
