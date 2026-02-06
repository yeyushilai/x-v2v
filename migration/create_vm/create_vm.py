# -*- coding: utf-8 -*-

"""
功能：创建虚拟机模块
"""

import os
import time
from logger import logger
from utils.cli.exec import normal_exec, bash_exec
from constants.template import CREATE_INSTANCE_INSERT_IMAGE_TEMPLATE
from constants.common import RunningDetailMigrateStatus
from exceptions import CreateVMError, handle_migration_exception


class CreateVM:
    """
    创建虚拟机类
    """

    def __init__(self, vm_session):
        self.vm_session = vm_session

    def create(self):
        """
        创建虚拟机
        """
        @handle_migration_exception(self.vm_session)
        def _create():
            logger.info("Starting to create VM: {vm_name}".format(
                vm_name=self.vm_session.dst_vm_name
            ))

            # 更新状态为创建中
            self.vm_session.update_detail_migrate_status({
                "running_detail_status": RunningDetailMigrateStatus.CREATE_VM.value
            })

            # 创建虚拟机
            vm_id = self._create_vm()
            self.vm_session.dst_vm_id = vm_id
            logger.info("VM created successfully with ID: {vm_id}".format(vm_id=vm_id))
            return True

        return _create()

    def _create_vm(self):
        """
        实际创建虚拟机的逻辑
        """
        # 构建创建虚拟机的命令
        create_cmd = self._build_create_cmd()
        logger.info("Create VM command: {cmd}".format(cmd=create_cmd))

        # 执行创建命令
        returncode, stdout, stderr = normal_exec(create_cmd)
        if returncode != 0:
            raise CreateVMError("Create VM failed: {stderr}".format(stderr=stderr))

        # 这里需要根据实际情况解析命令输出，获取虚拟机ID
        # 暂时返回一个占位符ID
        return "vm-" + str(int(time.time()))

    def _build_create_cmd(self):
        """
        构建创建虚拟机的命令
        """
        # 构建创建虚拟机的参数
        create_params = {
            "vm_name": self.vm_session.dst_vm_name,
            "vm_type": self.vm_session.dst_vm_type,
            "cpu": self.vm_session.dst_vm_cpu,
            "memory": self.vm_session.dst_vm_memory,
            "image_id": self.vm_session.dst_vm_image_id,
            "network": self.vm_session.dst_vm_net
        }

        # 构建创建命令
        create_cmd = CREATE_INSTANCE_INSERT_IMAGE_TEMPLATE.format(**create_params)
        return create_cmd

    def wait_for_vm_ready(self, vm_id, timeout=300):
        """
        等待虚拟机就绪
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 这里需要根据实际情况检查虚拟机状态
                logger.info("Checking VM {vm_id} status".format(vm_id=vm_id))
                # 假设检查成功
                return True
            except Exception as e:
                logger.warning("Failed to check VM status: {reason}".format(reason=str(e)))
                time.sleep(5)

        raise CreateVMError("Timeout waiting for VM to be ready")
