# -*- coding: utf-8 -*-

"""
功能：上传镜像模块
"""

import os
import time
from logger import logger
from utils.cli.exec import normal_exec, bash_exec
from constants.common import (
    UPLOAD_IMAGE_TIMEOUT,
    RunningDetailMigrateStatus
)
from exceptions import UploadImageError, handle_migration_exception


class UploadImage:
    """
    上传镜像类
    """

    def __init__(self, vm_session):
        self.vm_session = vm_session

    def upload(self):
        """
        上传镜像
        """
        @handle_migration_exception(self.vm_session)
        def _upload():
            logger.info("Starting to upload image for VM: {vm_name}".format(
                vm_name=self.vm_session.src_vm_name
            ))

            # 更新状态为上传中
            self.vm_session.update_detail_migrate_status({
                "running_detail_status": RunningDetailMigrateStatus.UPLOAD_IMAGE.value
            })

            # 构建上传命令
            upload_cmd = self._build_upload_cmd()
            logger.info("Upload command: {cmd}".format(cmd=upload_cmd))

            # 执行上传命令
            returncode, stdout, stderr = normal_exec(
                upload_cmd, timeout=UPLOAD_IMAGE_TIMEOUT
            )
            if returncode != 0:
                raise UploadImageError("Upload image failed: {stderr}".format(stderr=stderr))

            logger.info("Image uploaded successfully")
            return True

        return _upload()

    def _build_upload_cmd(self):
        """
        构建上传命令
        """
        # 这里需要根据实际的上传逻辑构建命令
        # 暂时返回一个占位符命令
        return "echo \"Uploading image {image_id}\" && sleep 1".format(
            image_id=self.vm_session.dst_vm_image_id
        )
