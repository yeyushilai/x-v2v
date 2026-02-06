# -*- coding: utf-8 -*-

"""
功能：处理镜像模块
"""

import os
import time
from logger import logger
from utils.cli.exec import normal_exec, bash_exec
from storage.nbd.tool import map_nbd_device_context, mount_nbd_device_context
from storage.qbd.tool import map_qbd_device_context
from constants.template import DEAL_IMAGE_CONVERT_IMAGE_CMD_TEMPLATE
from constants.common import RunningDetailMigrateStatus
from exceptions import DealImageError, handle_migration_exception


class DealImage:
    """
    处理镜像类
    """

    def __init__(self, vm_session):
        self.vm_session = vm_session

    def deal(self):
        """
        处理镜像
        """
        @handle_migration_exception(self.vm_session)
        def _deal():
            logger.info("Starting to deal with image for VM: {vm_name}".format(
                vm_name=self.vm_session.src_vm_name
            ))

            # 更新状态为处理中
            self.vm_session.update_detail_migrate_status({
                "running_detail_status": RunningDetailMigrateStatus.DEAL_IMAGE.value
            })

            # 转换镜像格式
            self._convert_image_format()
            logger.info("Image dealt successfully")
            return True

        return _deal()

    def _convert_image_format(self):
        """
        转换镜像格式
        """
        # 构建转换命令
        convert_cmd = DEAL_IMAGE_CONVERT_IMAGE_CMD_TEMPLATE.format(
            src_image_path=self._get_src_image_path(),
            dst_image_path=self._get_dst_image_path()
        )

        logger.info("Convert image command: {cmd}".format(cmd=convert_cmd))

        # 执行转换命令
        returncode, stdout, stderr = normal_exec(convert_cmd)
        if returncode != 0:
            raise DealImageError("Convert image failed: {stderr}".format(stderr=stderr))

    def _get_src_image_path(self):
        """
        获取源镜像路径
        """
        # 这里需要根据实际情况获取源镜像路径
        return os.path.join(self.vm_session.export_dir, "{vm_name}.ova".format(
            vm_name=self.vm_session.src_vm_name
        ))

    def _get_dst_image_path(self):
        """
        获取目标镜像路径
        """
        # 这里需要根据实际情况获取目标镜像路径
        return os.path.join(self.vm_session.upload_dir, "{vm_name}.qcow2".format(
            vm_name=self.vm_session.dst_vm_name
        ))

    def mount_image(self, image_path, mount_point):
        """
        挂载镜像
        """
        with map_nbd_device_context(image_path) as nbd_device:
            with mount_nbd_device_context(nbd_device, mount_point):
                logger.info("Image mounted successfully at: {mount_point}".format(
                    mount_point=mount_point
                ))
                # 在这里可以对挂载的镜像进行操作
                yield mount_point
