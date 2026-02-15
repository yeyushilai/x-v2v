# -*- coding: utf-8 -*-

"""
功能：迁移

功能分解：
1.导出镜像/上传镜像
2.处理镜像
3.创建虚拟机
4.覆盖镜像
5.修复调优
"""

import os
import datetime
import shutil
import tarfile
import time

from core.logger import logger
from core.config import config

# from clients.nfs_cli import NFSInterface
from tools.convert_tool import ConvertTool
from tools.time_tool import TimeTool
from tools.file_tool import FileTool
from tools.aes_tool import AESTool
from clients.cmd_cli import CMDClient

from constants.template import (
    # 导出镜像
    EXPORT_IMAGE_CMD_TEMPLATE,

    # 处理镜像
    DEAL_IMAGE_CONVERT_IMAGE_CMD_TEMPLATE,

    # 创建虚拟机
)

from constants.enum import (
    RunningDetailMigrateStatus,
    QemuImgAction,
    MigratePattern,
)

from error import ErrorMsg, ErrorCode


def copy_nfs_file(nfs_file_path, local_file_path, timeout=60):
    """从nfs拷贝文件到本地"""
    pass

def map_nbd_device_context(img_path):
    """连接到nbd设备，本质上是将镜像文件映射为nbd网络块设备"""
    pass


def mount_nbd_device_context(mnt_dir, dev_path, option="ro"):
    """ 挂载设备 """
    pass

class BaseMigration(object):

    def __init__(self, vm_session):
        self.vm_session = vm_session
        self.ovf_path = ""
        self.vmdk_path_list = list()

    def migrate(self):
        """开始迁移"""

        self.export_image()  # Note:只有导出镜像模式迁移才有此步骤
        self.upload_image()  # Note:只有上传镜像模式迁移才有此步骤
        self.deal_image()
        self.create_vm()
        self.cover_image()
        self.recorrect_and_optimize()


    def export_image(self):
        pass

    def upload_image(self):
        pass

    def deal_image(self):
        """处理镜像
        包括：
        1.解压镜像  Note:只有导出镜像模式迁移才有此步骤
        2.检查镜像  Note:只有导出镜像模式迁移才有此步骤
        3.生成目标虚拟机磁盘信息
        4.转换镜像格式
        """

        # 0.更新详细的迁移状态信息

        # 1.解压镜像
        self._uncompress_image()

        # 2.检查镜像
        self._check_image()

        # 3.生成目标虚拟机磁盘信息
        self._gen_dst_vm_disk_info()

        # 4.转换镜像格式
        self._convert_image()

        # 5.更新详细的迁移状态信息

    def create_vm(self):
        """创建虚拟机"""

        # 1.插入镜像数据
        self._insert_image()

        # 2.更新镜像资源计费信息
        self._update_resource_leasing()

        # 3.拷贝空镜像到存储节点
        self._copy_image_to_storage()

        # 4.创建目标虚拟机
        self._create_dst_vm()

        # # 5.关闭目标虚拟机
        self._stop_dst_vm()

        # 6.更新目标虚拟机镜像的状态为弃用
        self._update_dst_vm_image_status()

        # 7.从存储节点删除空镜像
        self._delete_image_from_seed()

        # 8.创建目标虚拟机的系统盘
        self._create_dst_vm_disks()

        # 9.加载目标虚拟机的系统盘
        self._attach_dst_vm_disks()

        # 10.更新详细的迁移状态信息

    def cover_image(self):
        """覆盖镜像"""
        
        # 更新详细的迁移状态信息

        # 存储部署模式:Sanc
        # Sanc 1.启动目标虚拟机
        self._start_dst_vm()

        # Sanc 2.使用mv, 覆盖系统盘
        self._cover_image_by_move(self.vm_session.dst_vm_os_disk)

        # Sanc 3.使用dd，覆盖数据盘
        for disk_info in self.vm_session.dst_vm_data_disk:
            self._cover_image_by_dd(disk_info)

        # Sanc 4.重启目标虚拟机
        self._restart_dst_vm()
        
        # 存储部署模式:普通
        # 普通 1.使用mv，覆盖所有的硬盘数据（包括系统盘和数据盘）
        for disk_info in self.vm_session.dst_vm_disk:
            self._cover_image_by_move(disk_info)

        # 普通 2.启动目标虚拟机
        self._start_dst_vm()

        # 更新详细的迁移状态信息

    def recorrect_and_optimize(self):
        """修复调优"""

        # 0.更新详细的迁移状态信息

        # 1.修复目标虚拟机驱动问题
        self._patch_drive()

        # 2.上传代理到目标虚拟机
        self._upload_proxy()

        # 3.更新详细的迁移状态信息

    def _uncompress_image(self):
        pass

    def _check_image(self):
        pass

    def _gen_dst_vm_disk_info(self):
        """生成目标虚拟机磁盘信息"""
        logger.info(f"generate dst vm disk info start, session id: {self.vm_session.session_id}")

        self.json_path = self.ovf_path.replace("ovf", "json")
        ovf_config = ConvertTool.xml_file_to_json_file(self.ovf_path, self.json_path)

        Envelope = ovf_config["Envelope"]

        # disk_id和disk_label的映射
        # example
        # {
        #   "vmdisk1": "Hard disk 1",
        #   "vmdisk2": "Hard disk 2"
        # }
        VirtualSystem = Envelope["VirtualSystem"]
        VirtualHardwareSection = VirtualSystem["VirtualHardwareSection"]
        Item = VirtualHardwareSection["Item"]
        disk_id_disk_label_mapper = dict()
        for item in Item:
            if "rasd:HostResource" in item.keys():
                HostResource = item[
                    "rasd:HostResource"]  # eg: "ovf:/disk/vmdisk1"
                resource = HostResource.split("/")[-1]  # eg: "vmdisk1"
                ElementName = item["rasd:ElementName"]  # eg: "Hard disk 1"
                disk_id_disk_label_mapper[resource] = ElementName
        logger.info(
            f"disk id and disk label mapper: {disk_id_disk_label_mapper}, "
            f"session id: {self.vm_session.session_id}, src vm id: {self.vm_session.src_vm_id}")

        # file_ref和disk_attr的映射
        # example:
        # {
        #     "file1": {
        #         "ovf_disk_id": "vmdisk1",
        #         "ovf_capacity": 100,
        #         "ovf_unit": "byte * 2^30",
        #     },
        #     "file2": {
        #         "ovf_disk_id": "vmdisk2",
        #         "ovf_capacity": 100,
        #         "ovf_unit": "byte * 2^30",
        #     }
        # }
        DiskSection = Envelope["DiskSection"]
        DiskSectionInfo = DiskSection["Disk"]
        file_ref_disk_attr_map = dict()
        # 若源虚拟机有单个硬盘
        if isinstance(DiskSectionInfo, dict):
            ovf_file_ref = DiskSectionInfo["@ovf:fileRef"]  # eg: "file1"
            ovf_disk_id = DiskSectionInfo["@ovf:diskId"]  # eg: "vmdisk1"
            ovf_capacity = DiskSectionInfo["@ovf:capacity"]  # eg: 100
            ovf_unit = DiskSectionInfo[
                "@ovf:capacityAllocationUnits"]  # byte * 2^30
            file_ref_disk_attr_map[ovf_file_ref] = dict(
                ovf_disk_id=ovf_disk_id,
                ovf_capacity=ovf_capacity,
                ovf_unit=ovf_unit)
        # 若源虚拟机有多个硬盘
        elif isinstance(DiskSectionInfo, list):
            for section in DiskSectionInfo:
                ovf_file_ref = section["@ovf:fileRef"]  # eg: "file1"
                ovf_disk_id = section["@ovf:diskId"]  # eg: "vmdisk1"
                ovf_capacity = section["@ovf:capacity"]  # eg: 100
                ovf_unit = section[
                    "@ovf:capacityAllocationUnits"]  # byte * 2^30
                file_ref_disk_attr_map[ovf_file_ref] = dict(
                    ovf_disk_id=ovf_disk_id,
                    ovf_capacity=ovf_capacity,
                    ovf_unit=ovf_unit)
        logger.info(f"file ref and disk attr mapper: {file_ref_disk_attr_map}, session id: {self.vm_session.session_id}, "
                    f"src vm id: {self.vm_session.src_vm_id}")

        # ovf_href和ovf_id的映射
        # example
        # {
        #   "xxxx-disk1.vmdk": "file1",
        #   "xxxx-disk2.vmdk": "file2"
        # }
        ovf_href_ovf_id_mapper = dict()
        References = Envelope["References"]
        File = References["File"]
        # 若源虚拟机有单个硬盘
        if isinstance(File, dict):
            ovf_id = File["@ovf:id"]  # eg: "file1"
            ovf_href = File["@ovf:href"]  # eg: "xxxx-disk1.vmdk""
            ovf_href_ovf_id_mapper[ovf_href] = ovf_id
        # 若源虚拟机有多个硬盘
        elif isinstance(File, list):
            for file_data in File:
                ovf_id = file_data["@ovf:id"]  # eg: "file1"
                ovf_href = file_data["@ovf:href"]  # eg: "xxxx-disk1.vmdk""
                ovf_href_ovf_id_mapper[ovf_href] = ovf_id
        logger.info(f"ovf href and ovf id mapper: {ovf_href_ovf_id_mapper}, "
                    f"session id: {self.vm_session.session_id}, src vm id: {self.vm_session.src_vm_id}")

        # vmdk文件名称和vmdk文件路径的映射
        # example:
        # {
        #   'xxxx-disk1.vmdk': '/xxxx/v2v_export/session-xxxx/xxxx/xxxx-disk1.vmdk',
        #   'xxxx-disk2.vmdk': '/xxxx/v2v_export/session-xxxx/xxxx/xxxx-disk2.vmdk'
        # }
        dst_vm_disk = list()
        try:
            for vmdk_path in self.vmdk_path_list:
                disk_info = dict()
                decode_vmdk_name = os.path.basename(vmdk_path).decode("utf8")
                decode_vmdk_path = vmdk_path.decode("utf8")
                ovf_id = ovf_href_ovf_id_mapper[decode_vmdk_name]
                ovf_disk_id = file_ref_disk_attr_map[ovf_id]["ovf_disk_id"]
                ovf_capacity = file_ref_disk_attr_map[ovf_id]["ovf_capacity"]
                ovf_unit = file_ref_disk_attr_map[ovf_id]["ovf_unit"]
                disk_label = disk_id_disk_label_mapper[ovf_disk_id]

                disk_info["vmdk_name"] = decode_vmdk_name  # xxxx-disk1.vmdk
                disk_info[
                    "vmdk_path"] = decode_vmdk_path  # /xxxx/v2v_export/session-xxxx/xxxx/xxxx-disk1.vmdk
                disk_info["vmdk_size"] = FileTool.get_file_size(
                    decode_vmdk_path)  # 单位MB
                disk_info["ovf_id"] = ovf_id  # file1
                disk_info["ovf_disk_id"] = ovf_disk_id  # vmdisk1
                disk_info["name"] = disk_label  # Hard disk 1
                disk_info["name"] = disk_label  # Hard disk 1

                # 容量单位转换
                if ovf_unit == "byte * 2^30":
                    # 默认为GB
                    src_size = int(round(float(ovf_capacity)))
                elif ovf_unit == "byte * 2^20":
                    # MB转换为GB
                    src_size = int(round(float(ovf_capacity))) / 1024
                elif ovf_unit == "byte * 2^10":
                    # KB转换为GB
                    src_size = int(round(float(ovf_capacity))) / 1024 / 1024
                elif ovf_unit == "byte":
                    # B转换为GB
                    src_size = int(
                        round(float(ovf_capacity))) / 1024 / 1024 / 1024
                else:
                    # 默认为GB
                    src_size = int(round(float(ovf_capacity)))

                # 容量为10的倍数处理
                src_size_suffix = int(str(src_size)[-1])
                if src_size_suffix == 0:
                    disk_info["size"] = src_size  # 100GB
                else:
                    disk_info["size"] = int(src_size) + (
                                10 - src_size_suffix)  # 100GB

                dst_vm_disk.append(disk_info)
        except Exception as e:
            self.vm_session.update_detail_migrate_status(dict(
                err_code=ErrorCode.DEAL_IMAGE_ERROR_DISK_CONFIG_RELATE_IMAGE_PATH.value,
                err_msg=ErrorMsg.DEAL_IMAGE_ERROR_DISK_CONFIG_RELATE_IMAGE_PATH.value.zh))

            log_msg = f"generate dst vm disk info failed, session id: {self.vm_session.session_id}, dst vm disk: {dst_vm_disk}, error reason: {str(e)}"
            logger.exception(log_msg)
            raise Exception(log_msg)

        # 更新配置到数据库
        self.vm_session.update_to_mem_and_pg(dict(dst_vm_disk=dst_vm_disk))
        logger.info(f"generate dst vm disk info end, session id: {self.vm_session.session_id}, dst vm disk: {dst_vm_disk}")

    def _convert_image(self):
        """转换镜像"""
        logger.info(f"convert image start, session id: {self.vm_session.session_id}, dst vm disk: {self.vm_session.dst_vm_disk}")

        dst_vm_disk = self.vm_session.dst_vm_disk
        for disk_info in dst_vm_disk:
            vmdk_path = disk_info["vmdk_path"]
            disk_info["qcow2_path"] = qcow2_path = vmdk_path.replace("vmdk",
                                                                     "qcow2")

            # 执行转换镜像命令
            convert_cmd = f"{config.migration.qemu_img_tool_path} {QemuImgAction.CONVERT.value} -p -f {config.migration.deal_image_src_format_vmdk} -O {config.migration.deal_image_dst_format_qcow2} {vmdk_path} {qcow2_path}"
            logger.info(f"convert image ready, session id: {self.vm_session.session_id}, disk name: {disk_info['name']}, convert cmd: {convert_cmd}")
            returncode, _, stderr = CMDClient.bash_exec(convert_cmd, config.migration.convert_image_timeout)
            if returncode != 0:
                self.vm_session.update_detail_migrate_status(dict(
                    err_code=ErrorCode.CONVERT_IMAGE_ERROR_COMMON.value,
                    err_msg=ErrorMsg.CONVERT_IMAGE_ERROR_COMMON.value.zh))
                log_msg = f"convert image failed, session id: {self.vm_session.session_id}, disk name: {disk_info['name']}, convert cmd: {convert_cmd}, error reason: {stderr}"
                logger.error(log_msg)
                raise Exception(log_msg)

            # 删掉原始的vmdk文件，节省空间
            disk_info["qcow2_size"] = FileTool.get_file_size(qcow2_path)
            os.remove(vmdk_path)

            # 统计信息

            # 识别系统盘并赋值
            is_os_disk = disk_info.get("is_os_disk",
                                       None) or self.identify_src_vm_os_disk(
                qcow2_path)
            disk_info["is_os_disk"] = is_os_disk
            if is_os_disk:
                disk_info["volume_type"] = \
                self.vm_session.info["dst_vm_os_disk"]["type"]
            else:
                if "dst_vm_data_disk" in self.vm_session.info \
                        and isinstance(
                    self.vm_session.info["dst_vm_data_disk"], dict) \
                        and "type" in self.vm_session.info["dst_vm_data_disk"]:
                    data_disk_type = self.vm_session.info["dst_vm_data_disk"][
                        "type"]
                    disk_info["volume_type"] = data_disk_type



            # 更新虚拟机的配置

        # 若源虚拟机没有安装系统，则直接报错，迁移终止
    
        # 若源虚拟机识别错误识别出来多个系统盘，则直接报错，迁移终止

        # 更新虚拟机的配置

    def _insert_image(self):
        """插入镜像数据"""

    def _update_resource_leasing(self):
        """更新资源计费信息"""

    def _copy_image_to_storage(self):
        """拷贝镜像到存储节点"""

    def _delete_image_from_storage(self):
        """从存储节点删除镜像"""

    def _create_dst_vm(self):
        """创建虚拟机"""

    def _describe_instance(self):
        """查询虚拟机"""

    def _start_dst_vm(self):
        """启动目标虚拟机"""

    def _restart_dst_vm(self):
        """重启虚拟机"""

    def _stop_dst_vm(self):
        """关闭虚拟机"""

    def _update_dst_vm_image_status(self):
        """更新镜像状态"""

    def _create_dst_vm_disks(self):
        """创建硬盘
        Note:只有数据盘需要创建
        """

    def _attach_dst_vm_disks(self):
        """加载硬盘
        Note:只有数据盘需要加载
        """

    def _cover_image_by_move(self, disk_info):
        """通过剪切的方式覆盖镜像"""
    

    def _cover_image_by_dd(self, disk_info):
        """通过dd的方式覆盖镜像"""

    def identify_src_vm_os_disk(self, qcow2_path):
        is_os_disk = self._identify_src_vm_os_disk(qcow2_path)
        if is_os_disk is not None:
            return is_os_disk

        # 走到这里，意味着当前的方法均无法判断
        self.vm_session.update_detail_migrate_status(dict(
            err_code=ErrorCode.CONVERT_IMAGE_ERROR_IDENTIFY_OS_DISK_FAILED.value,
            err_msg=ErrorMsg.CONVERT_IMAGE_ERROR_IDENTIFY_OS_DISK_FAILED.value.zh))
        log_msg = f"identify os disk failed, image file: {qcow2_path}, error reason: {ErrorMsg.CONVERT_IMAGE_ERROR_IDENTIFY_OS_DISK_FAILED.value.en}"
        logger.error(log_msg)
        raise Exception(log_msg)

    def _identify_src_vm_os_disk(self, qcow2_path):
        """识别镜像文件关联的硬盘是否为系统盘"""

        if self.vm_session.dst_vm_disk_num == 1:
            return True

        with map_nbd_device_context(qcow2_path) as img_info:
            if not img_info["has_partition"]:
                return False
            pass


    @staticmethod
    def _identify_windows_os_disk_by_boot(img_info):
        """windows操作系统依据boot文件判断是否为系统盘"""
        partition_info = img_info["partition_info"]

        tag_file_list = ["bootx64.efi", "boot.ini", "AUTOEXEC.BAT"]
        for indeed_dev_path, partition_mnt_dir in partition_info.items():
            os.makedirs(partition_mnt_dir) if not os.path.isdir(
                partition_mnt_dir) else None

            # 挂载，读取内容并判断是否为系统盘
            with mount_nbd_device_context(partition_mnt_dir,
                                          indeed_dev_path) as is_success:
                if not is_success:
                    continue

                if "Windows" in os.listdir(partition_mnt_dir):
                    return True

                if "Boot" in os.listdir(partition_mnt_dir):
                    return True

                if "Program Files" in os.listdir(partition_mnt_dir):
                    return True

                if FileTool.find_file(partition_mnt_dir, tag_file_list, False):
                    return True
        else:
            return False

    def _identify_linux_os_disk_by_fdisk(self, img_info):
        """linux操作系统依据fdisk命令判断是否为系统盘"""
        dev_path = img_info["dev_path"]
        cmd = f"fdisk -l {dev_path} | grep {dev_path} | grep -v 'Linux LVM' | grep -E 'Linux|W95 FAT32' | awk -F ' ' '{{print $2}}'"
        returncode, stdout, stderr = CMDClient.normal_exec(cmd)
        if returncode == 0:
            if stdout:
                logger.info(f"get suitable boot info, session id: {self.vm_session.session_id}, boot info: {stdout}")
                if "*" in stdout.split("\n"):
                    return True

        partition_info = img_info["partition_info"]
        for indeed_dev_path, partition_mnt_dir in partition_info.items():
            os.makedirs(partition_mnt_dir) if not os.path.isdir(
                partition_mnt_dir) else None

            # 挂载，读取内容并判断是否为系统盘
            with mount_nbd_device_context(partition_mnt_dir,
                                          indeed_dev_path) as is_success:
                if not is_success:
                    continue

                if "boot" in os.listdir(partition_mnt_dir):
                    return True

                if "root" in os.listdir(partition_mnt_dir):
                    return True

                if "EFI" in os.listdir(partition_mnt_dir):
                    return True

                if "grub" in os.listdir(partition_mnt_dir):
                    return True
        else:
            return False

    def _patch_drive(self):
        """处理驱动问题"""
        pass

    def _upload_proxy(self):
        """上传代理"""
        pass


class ExportImageMigration(BaseMigration):
    """导出镜像模式对应的迁移器"""
    migrate_pattern = MigratePattern.EXPORT_IMAGE.value

    def __init__(self, vm_session):
        super(ExportImageMigration, self).__init__(vm_session)
        self.ova_path = ""

    def export_image(self):
        """导出镜像"""
        logger.info(f"export image start, session id: {self.vm_session.session_id}, src vm name: {self.vm_session.src_vm_name}")
        # 更新详细的迁移状态信息
        start_status = RunningDetailMigrateStatus.START_EXPORT_IMAGE_DETAIL_STATUS.value
        start_status["step"]["start_time"] = TimeTool.get_now_datetime_str()
        self.vm_session.update_detail_migrate_status(start_status)

        """
        命令格式
        {ovf_tool_path} {cmd_params} 
        '{cmd_prefix}{username}:{password}@{ip}:{port}/{datacenter}/{vm_dir}/{vm_folder}/{src_vm_name}' 
        {dst_dir}/{dst_vm_name}.{dst_image_format}
        """

        # 目前写死， 后续再酌情优化
        disk_mode_param = "--diskMode=thin"
        advanced_params = " ".join([disk_mode_param])

        src_platform = self.vm_session.task.src_platform
        export_image_cmd = f"{config.migration.ovf_tool_path} {config.migration.export_image_common_params} {advanced_params} '{config.migration.export_image_cmd_prefix}{src_platform.user}:{AESTool.aes_decode(src_platform.password)}@{src_platform.ip}:{src_platform.port}/{self.vm_session.task.src_datacenter_name}/vm/{self.vm_session.src_vm_folder}/{self.vm_session.src_vm_name}' '{self.vm_session.export_dir}/{self.vm_session.dst_vm_name}.{config.migration.export_image_dst_format.value}' "
        logger.info(f"export image ready, session id: {self.vm_session.session_id}, src vm name: {self.vm_session.src_vm_name}, export image cmd: {export_image_cmd}")
        start_time = datetime.datetime.now()

        # 执行导出镜像命令
        execute_times = 0
        while True:
            execute_times += 1
            logger.info(
                f"export image, execute times: {execute_times} times, max retry times: {config.migration.export_image_max_retry_times} times, session id: {self.vm_session.session_id}")
            returncode, stdout, stderr = CMDClient.normal_exec(export_image_cmd, config.migration.export_image_timeout)
            if returncode == 0:
                break

            if execute_times >= config.migration.export_image_max_retry_times:
                self.vm_session.update_detail_migrate_status(dict(
                    err_code=ErrorCode.EXPORT_IMAGE_ERROR_COMMON.value,
                    err_msg=ErrorMsg.EXPORT_IMAGE_ERROR_COMMON.value.zh))

                log_msg = f"export image failed, retry times has out of limit, session id: {self.vm_session.session_id}, export image cmd: {export_image_cmd}, error reason: {stderr}"
                logger.error(log_msg)
                raise Exception(log_msg)
            time.sleep(10)

        # 检查OVA文件是否成功下载
        ova_name = ".".join(
            [self.vm_session.dst_vm_name, config.migration.export_image_dst_format.value])
        self.ova_path = os.path.join(self.vm_session.export_dir, ova_name)
        if not os.path.isfile(self.ova_path):
            self.vm_session.update_detail_migrate_status(dict(
                err_code=ErrorCode.EXPORT_IMAGE_ERROR_OVA_NOT_EXISTS.value,
                err_msg=ErrorMsg.EXPORT_IMAGE_ERROR_OVA_NOT_EXISTS.value.zh))

            log_msg = f"export image failed, can not find ova file, session id: {self.vm_session.session_id}, ova path: {self.ova_path}"
            logger.error(log_msg)
            raise Exception(log_msg)

        # 更新详细的迁移状态信息
        end_status = RunningDetailMigrateStatus.END_EXPORT_IMAGE_DETAIL_STATUS.value
        end_status["step"]["end_time"] = TimeTool.get_now_datetime_str()
        self.vm_session.update_detail_migrate_status(end_status)

        # 统计数据
        end_time = datetime.datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        time_strftime = str(datetime.timedelta(seconds=total_seconds))
        ova_size = FileTool.get_file_size(self.ova_path)
        export_speed = ova_size / total_seconds  # 单位：MB/s
        logger.info(f"export image end, session id: {self.vm_session.session_id}, cost time: {time_strftime}, execute times: {execute_times} times, "
                    f"ova size: {ova_size}MB, export speed: {export_speed}MB/s, ova path: {self.ova_path}")

    def _uncompress_image(self):
        """解压镜像"""
        logger.info(f"uncompress image start, session id: {self.vm_session.session_id}, ova path: {self.ova_path}")
        vmdk_dir = os.path.join(self.vm_session.export_dir,
                                self.vm_session.dst_vm_name)
        shutil.rmtree(vmdk_dir) if os.path.isdir(vmdk_dir) else None
        os.mkdir(vmdk_dir)
        start_time = datetime.datetime.now()
        try:
            tar = tarfile.open(self.ova_path)
            for single_file in tar.getnames():
                if single_file.endswith("ovf"):
                    tar.extract(single_file, self.vm_session.export_dir)
                    self.ovf_path = os.path.join(self.vm_session.export_dir,
                                                 single_file)
                elif single_file.endswith("vmdk"):
                    tar.extract(single_file, vmdk_dir)
                    self.vmdk_path_list.append(
                        os.path.join(vmdk_dir, single_file))
                elif single_file.endswith("mf"):
                    tar.extract(single_file, self.vm_session.export_dir)
                    self.mf_path = os.path.join(self.vm_session.export_dir,
                                                single_file)
                else:
                    continue
            tar.close()
        except Exception as e:
            self.vm_session.update_detail_migrate_status(dict(
                err_code=ErrorCode.DEAL_IMAGE_ERROR_UNCOMPRESS_IMAGE_FAILED.value,
                err_msg=ErrorMsg.DEAL_IMAGE_ERROR_UNCOMPRESS_IMAGE_FAILED.value.zh))

            log_msg = f"uncompress image failed, user id: {self.vm_session.user_id}, session id: {self.vm_session.session_id}, ova path: {self.ova_path}, error reason: {str(e)}"
            logger.error(log_msg)
            raise Exception(log_msg)

        # 记录结束时间并统计
        end_time = datetime.datetime.now()
        total_seconds = (end_time - start_time).total_seconds()
        time_strftime = str(datetime.timedelta(seconds=total_seconds))
        ova_size = FileTool.get_file_size(self.ova_path)
        uncompress_speed = ova_size / total_seconds  # 单位: MB/s

        logger.info(f"uncompress image end, session id: {self.vm_session.session_id}, cost time: {time_strftime}, ova_size: {ova_size}MB, uncompress speed: {uncompress_speed}MB/s, ova path: {self.ova_path}, "
                    f"vmdk path list: {self.vmdk_path_list}, ovf path: {self.ovf_path}")

    def check_image(self):
        """检查镜像"""
        return self._check_image()

    def _check_image(self):
        """检查镜像
        # 1.完整性检查
        # 2.检查文件的SHA256值
        """

        logger.info(f"check image start, session id: {self.vm_session.session_id}, ova path: {self.ova_path}, mf path: {self.mf_path}")
        if not self.mf_path:
            self.vm_session.update_detail_migrate_status(dict(
                err_code=ErrorCode.DEAL_IMAGE_ERROR_MF_NOT_EXISTS.value,
                err_msg=ErrorMsg.DEAL_IMAGE_ERROR_MF_NOT_EXISTS.value.zh))

            log_msg = f"mf file is not exists, session id: {self.vm_session.session_id}"
            logger.error(log_msg)
            raise Exception(log_msg)

        mf_data = {}
        mf_content = FileTool.read_file(self.mf_path)
        items = mf_content.split("\n")
        for line in items:
            if line:
                key, value = line.split("=")
                if key not in mf_data:
                    mf_data[key] = value.strip()
        logger.info(f"mf data: {mf_data}, session id: {self.vm_session.session_id}")

        # 检查ovf文件
        ovf_name = os.path.basename(self.ovf_path)
        ovf_key = f"SHA256({ovf_name})"
        ovf_content = FileTool.read_file(self.ovf_path)
        ovf_sha256 = FileTool.sha256_tool(ovf_content)
        if mf_data.get(ovf_key) != ovf_sha256:
            self.vm_session.update_detail_migrate_status(dict(
                err_code=ErrorCode.DEAL_IMAGE_ERROR_OVF_NOT_MATCH.value,
                err_msg=ErrorMsg.DEAL_IMAGE_ERROR_OVF_NOT_MATCH.value.zh))

            log_msg = f"ovf file {ovf_name} md5 is not match, mf md5: {mf_data.get(ovf_key)}, ovf md5: {ovf_sha256}"
            logger.error(log_msg)
            raise Exception(log_msg)

        # 检查vmdk文件
        for vmdk_path in self.vmdk_path_list:
            vmdk_name = os.path.basename(vmdk_path)
            vmdk_key = f"SHA256({vmdk_name})"
            vmdk_content = FileTool.read_file(vmdk_path)
            vmdk_sha256 = FileTool.sha256_tool(vmdk_content)
            if mf_data.get(vmdk_key) != vmdk_sha256:
                self.vm_session.update_detail_migrate_status(dict(
                    err_code=ErrorCode.DEAL_IMAGE_ERROR_VMDK_NOT_MATCH.value,
                    err_msg=ErrorMsg.DEAL_IMAGE_ERROR_VMDK_NOT_MATCH.value.zh))

                log_msg = f"vmdk file {ovf_name} md5 is not match, mf md5: {mf_data.get(ovf_key)}, vmdk md5: {vmdk_sha256}"
                logger.error(log_msg)
                raise Exception(log_msg)

        logger.info(f"check image end, session id: {self.vm_session.session_id}, ova path: {self.ova_path}, mf path: {self.mf_path}")


class UploadImageMigration(BaseMigration):
    """上传镜像模式对应的迁移器"""
    migrate_pattern = MigratePattern.UPLOAD_IMAGE.value

    def __init__(self, vm_session):
        super(UploadImageMigration, self).__init__(vm_session)

    def upload_image(self):
        """上传镜像"""
        # logger.info("upload image start, session id: {session_id}"
        #             .format(session_id=self.vm_session.session_id))
        # # 更新详细的迁移状态信息
        # start_status = RunningDetailMigrateStatus.START_UPLOAD_IMAGE_DETAIL_STATUS.value
        # start_status["step"]["start_time"] = TimeTool.get_now_datetime_str()
        # self.vm_session.update_detail_migrate_status(start_status)

        # start_time = datetime.datetime.now()
        # try:
        #     src_vm_nfs_path = self.vm_session.src_vm_nfs_path
        #     dst_vm_name = self.vm_session.dst_vm_name
        #
        #     # 初始化vmdk目录
        #     vmdk_dir = os.path.join(self.vm_session.upload_dir, dst_vm_name)
        #     shutil.rmtree(vmdk_dir) if os.path.isdir(vmdk_dir) else None
        #     os.mkdir(vmdk_dir)
        #
        #     total_size = 0
        #     nfs = NFSInterface(src_vm_nfs_path)
        #     for single_file in nfs.listdirs(""):
        #         file_path = os.path.join(src_vm_nfs_path, single_file)
        #         if single_file.endswith('ovf'):
        #             self.ovf_path = os.path.join(self.vm_session.upload_dir,
        #                                          single_file)
        #             copy_nfs_file(file_path, self.ovf_path)
        #             total_size += os.path.getsize(self.ovf_path)
        #         elif single_file.endswith('vmdk'):
        #             vmdk_path = os.path.join(vmdk_dir, single_file)
        #             copy_nfs_file(file_path, vmdk_path,
        #                           timeout=config.migration.upload_image_timeout.value)
        #             total_size += os.path.getsize(vmdk_path)
        #             self.vmdk_path_list.append(vmdk_path)
        # except Exception as e:
        #     self.vm_session.update_detail_migrate_status(dict(
        #         err_code=ErrorCode.UPLOAD_IMAGE_ERROR_COMMON.value,
        #         err_msg=ErrorMsg.UPLOAD_IMAGE_ERROR_COMMON.value.zh))
        #
        #     log_msg = "upload image failed, session id: {session_id}, error " \
        #               "reason: {error_reason}" \
        #               "".format(session_id=self.vm_session.session_id,
        #                         error_reason=str(e))
        #     logger.exception(log_msg)
        #     raise Exception(log_msg)
        #
        # # 更新详细的迁移状态信息
        # end_status = RunningDetailMigrateStatus.END_UPLOAD_IMAGE_DETAIL_STATUS.value
        # end_status["step"]["end_time"] = TimeTool.get_now_datetime_str()
        # self.vm_session.update_detail_migrate_status(end_status)
        #
        # # 汇总数据
        # end_time = datetime.datetime.now()
        # total_seconds = (end_time - start_time).total_seconds()
        # time_strftime = str(datetime.timedelta(seconds=total_seconds))
        # total_size = round(total_size / float(1024 * 1024), 2)
        # upload_speed = total_size / total_seconds  # 单位：MB/s
        # logger.info("upload image end, session id: {session_id}, cost_time: "
        #             "{cost_time}, total_size: {total_size}MB, upload speed: "
        #             "{upload_speed}MB/s"
        #             .format(cost_time=time_strftime,
        #                     total_size=total_size,
        #                     upload_speed=upload_speed,
        #                     session_id=self.vm_session.session_id))
