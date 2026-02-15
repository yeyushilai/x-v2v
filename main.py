#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.logger import logger
from vm_session import VMSession


class MigrateHandler:
    """ 迁移Handler类 """

    action = "immediately_migrate"

    def __init__(self, params):
        self.vm_session_info = params

    def start(self):
        """发起迁移"""
        session_id = self.vm_session_info["session_id"]
        user_id = self.vm_session_info["user_id"]

        logger.info("=====================================")
        logger.info(
            f"vm start migrate, session id: {session_id}, "
            f"action: {self.action}, user id: {user_id}"
        )
        vm_session = VMSession(session_id)
        vm_session.info = self.vm_session_info
        vm_session.migrate()


if __name__ == "__main__":
    params = {
        # ===== 核心标识 =====
        "session_id": "session-12345678-1234-5678-1234-567812345678",
        "task_id": "task-12345678-1234-5678-1234-567812345678",
        "user_id": "usr-abc12345",
        # ===== 源虚拟机信息 (VMware) =====
        "src_vm_id": "vm-123456",
        "src_vm_name": "test-vm-01",
        "src_vm_cpu_core": 2,
        "src_vm_memory": 4096,
        "src_vm_os_type": "windows",
        "src_vm_os_name": "Windows Server 2019",
        "src_vm_folder": "/Datacenter/vm",
        "src_vm_nfs_path": "",
        "src_vm_create_time": "2024-01-01T00:00:00",
        # ===== 源虚拟机磁盘配置 (src_vm_disk) =====
        "src_vm_disk": [
            {
                "device_key": 2000,
                "file_path": "[datastore1] test-vm-01/test-vm-01.vmdk",
                "capacity": 50,
                "controller_key": 1000,
                "unit_number": 0,
                "disk_mode": "persistent",
                "thin_provisioned": True,
                "controller_type": "lsilogic",
            },
            {
                "device_key": 2001,
                "file_path": "[datastore1] test-vm-01/test-vm-01_1.vmdk",
                "capacity": 100,
                "controller_key": 1000,
                "unit_number": 1,
                "disk_mode": "persistent",
                "thin_provisioned": True,
                "controller_type": "lsilogic",
            },
            {
                "device_key": 2002,
                "file_path": "[datastore2] test-vm-01/test-vm-01_2.vmdk",
                "capacity": 200,
                "controller_key": 1001,
                "unit_number": 0,
                "disk_mode": "independent_persistent",
                "thin_provisioned": False,
                "controller_type": "paravirtual",
            },
        ],
        # ===== 源虚拟机网络配置 =====
        "src_vm_net": [
            {
                "mac_address": "00:50:56:AA:BB:CC",
                "network_name": "VM Network",
                "adapter_type": "e1000",
                "connected": True,
                "start_connected": True,
            },
            {
                "mac_address": "00:50:56:DD:EE:FF",
                "network_name": "VM Network 2",
                "adapter_type": "vmxnet3",
                "connected": True,
                "start_connected": True,
            },
        ],
        # ===== 目标虚拟机配置 =====
        "dst_vm_name": "migrated-vm-01",
        "dst_vm_type": "s2.small",
        "dst_vm_cpu_core": 2,
        "dst_vm_memory": 4096,
        "dst_vm_os_type": "windows",
        "dst_vm_os_name": "Windows Server 2019",
        # ===== 目标镜像配置 =====
        "dst_vm_image": {
            "image_id": "img-12345678-1234-5678-1234-567812345678",
            "image_name": "image-test-windows-2019",
            "os_type": "windows",
            "platform": "windows",
            "processor_type": "x86_64",
            "size": 50,
        },
        # ===== 目标磁盘配置 (dst_vm_disk) =====
        "dst_vm_disk": [
            {
                "size": 50,
                "device_name": "/dev/sda",
                "volume_id": "vol-00000001",
                "volume_name": "system-disk",
                "disk_type": 0,
            },
            {
                "size": 100,
                "device_name": "/dev/sdb",
                "volume_id": "vol-00000002",
                "volume_name": "data-disk-1",
                "disk_type": 2,
            },
            {
                "size": 200,
                "device_name": "/dev/sdc",
                "volume_id": "vol-00000003",
                "volume_name": "data-disk-2",
                "disk_type": 2,
            },
        ],
        "dst_vm_os_disk": {"type": 0, "size": 50, "volume_name": "system-disk"},
        "dst_vm_data_disk": {"type": 2, "count": 2},
        # ===== 目标网络配置 (dst_vm_net) =====
        "dst_vm_net": [
            {
                "vxnet_id": "vxnet-12345678",
                "vxnet_type": 1,
                "vxnet_name": "私有网络",
                "vpc_router_id": "rtr-12345678",
                "router": "192.168.1.1",
                "ip": "192.168.1.100",
            },
            {
                "vxnet_id": "vxnet-87654321",
                "vxnet_type": 0,
                "vxnet_name": "公有网络",
                "vpc_router_id": "",
                "router": "",
                "ip": "",
            },
        ],
        # ===== 迁移状态 =====
        "status": "ready",
        "process": 0,
        "step": {},
        "priority": 1,
        # ===== 目标节点信息 (初始化时会填充) =====
        "indeed_dst_node_id": "",
        "indeed_dst_node_ip": "",
        # ===== 额外信息 (初始化时会添加) =====
        "extra": {},
    }

    handler = MigrateHandler(params)
    handler.start()
