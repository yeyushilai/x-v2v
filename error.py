# -*- coding: utf-8 -*-

from enum import Enum


class ErrorCode(Enum):
    # 成功
    SUCCESS = 0

    # 通用错误
    ERROR_COMMON = 1
    ERROR_WORKER_SERVICE_RESET = 2
    ERROR_DISPATCH_START_MIGRATE_TIMEOUT = 4
    ERROR_DISPATCH_END_MIGRATE_TIMEOUT = 5
    ERROR_DST_VM_TYPE_INVALID = 6
    ERROR_DST_VM_VOLUME_TYPE_INVALID = 7

    # 前置检查
    PRECHECK_ERROR_COMMON = 1000
    PRECHECK_ERROR_SRC_VM_STATUS_INVALID = 1001
    PRECHECK_ERROR_OVF_COUNT_INVALID = 1002
    PRECHECK_ERROR_VMDK_COUNT_INVALID = 1003
    PRECHECK_ERROR_DST_VM_OS_TYPE_INVALID = 1004
    PRECHECK_ERROR_DST_VM_BOOT_LOADER_TYPE_INVALID = 1005
    PRECHECK_ERROR_DST_VM_BLOCK_BUS_TYPE_INVALID = 1006
    PRECHECK_ERROR_DST_VM_NET_TYPE_INVALID = 1007
    PRECHECK_ERROR_DST_VM_MEMORY_VALUE_INVALID = 1008
    PRECHECK_ERROR_DST_VM_CPU_VALUE_INVALID = 1009
    PRECHECK_ERROR_STC_VM_NFS_PATH_EMPTY = 1010

    # 导出镜像
    EXPORT_IMAGE_ERROR_COMMON = 2000
    EXPORT_IMAGE_ERROR_OVA_NOT_EXISTS = 2001

    # 上传镜像
    UPLOAD_IMAGE_ERROR_COMMON = 3000

    # 处理镜像
    DEAL_IMAGE_ERROR_COMMON = 4000
    DEAL_IMAGE_ERROR_MF_NOT_EXISTS = 4001
    DEAL_IMAGE_ERROR_OVF_NOT_MATCH = 4002
    DEAL_IMAGE_ERROR_VMDK_NOT_MATCH = 4003
    DEAL_IMAGE_ERROR_DISK_CONFIG_RELATE_IMAGE_PATH = 4004
    DEAL_IMAGE_ERROR_UNCOMPRESS_IMAGE_FAILED = 4005
    CONVERT_IMAGE_ERROR_COMMON = 5000
    CONVERT_IMAGE_ERROR_IDENTIFY_OS_DISK_FAILED = 5001
    CONVERT_IMAGE_ERROR_OS_DISK_NOT_EXISTS = 5002
    CONVERT_IMAGE_ERROR_MULTI_OS_DISK_EXISTS = 5003

    # 创建虚拟机
    REGISTER_IMAGE_ERROR_COMMON = 6000
    REGISTER_IMAGE_ERROR_UNKNOWN_VM_TYPE = 6001
    CREATE_INSTANCE_ERROR_COMMON = 7000
    CREATE_INSTANCE_ERROR_RUN_INSTANCE_FAILED = 7001
    CREATE_INSTANCE_ERROR_UPDATE_USER_QUOTAS_FAILED = 7002
    CREATE_INSTANCE_ERROR_DESCRIBE_INSTANCE_FAILED = 7003
    CREATE_INSTANCE_ERROR_START_INSTANCE_FAILED = 7004
    CREATE_INSTANCE_ERROR_STOP_INSTANCE_FAILED = 7005
    CREATE_INSTANCE_ERROR_CREATE_VOLUMES_FAILED = 7006
    CREATE_INSTANCE_ERROR_ATTACH_VOLUMES_FAILED = 7007
    CREATE_INSTANCE_ERROR_COVER_IMAGES_TO_VOLUMES_FAILED = 7008
    CREATE_INSTANCE_ERROR_UPDATE_IMAGE_STATUS_FAILED = 7009
    CREATE_INSTANCE_ERROR_START_INSTANCE_TIMEOUT = 7010
    CREATE_INSTANCE_ERROR_STOP_INSTANCE_TIMEOUT = 7011
    CREATE_INSTANCE_ERROR_VOLUME_NOT_EXISTS = 7012
    CREATE_INSTANCE_ERROR_RESTART_INSTANCE_FAILED = 7013
    CREATE_INSTANCE_ERROR_copy_image_to_storage_FAILED = 7014

    # 覆盖镜像
    COVER_IMAGE_ERROR_COMMON = 8000

    # 修复调优
    RECORRECT_AND_OPTIMIZE_ERROR_COMMON = 9000


class _ErrorDict:
    def __init__(self, en: str, zh: str):
        self.en = en
        self.zh = zh
    
    def __getitem__(self, key: str):
        if key == "en":
            return self.en
        elif key == "zh":
            return self.zh
        raise KeyError(key)


class ErrorMsg(Enum):
    # 成功
    SUCCESS = _ErrorDict("", "")

    # 通用错误
    ERROR_COMMON = _ErrorDict("common error", "程序通用错误")
    ERROR_WORKER_SERVICE_RESET = _ErrorDict("worker service reset", "迁移服务被重置")
    ERROR_DISPATCH_START_MIGRATE_TIMEOUT = _ErrorDict("dispatch start migrate timeout", "调度开始迁移超时")
    ERROR_DISPATCH_END_MIGRATE_TIMEOUT = _ErrorDict("dispatch end migrate timeout", "调度结束迁移超时")
    ERROR_DST_VM_TYPE_INVALID = _ErrorDict("dst vm type invalid", "目标虚拟机类型非法")
    ERROR_DST_VM_VOLUME_TYPE_INVALID = _ErrorDict("dst vm volume type invalid", "目标虚拟机硬盘类型非法")

    # 前置检查
    PRECHECK_ERROR_COMMON = _ErrorDict("migrate precheck failed", "迁移前的前置检查失败")
    PRECHECK_ERROR_SRC_VM_STATUS_INVALID = _ErrorDict("src vm status invalid", "源虚拟机的状态非法")
    PRECHECK_ERROR_OVF_COUNT_INVALID = _ErrorDict("ovf file count invalid", "OVF文件数量非法")
    PRECHECK_ERROR_VMDK_COUNT_INVALID = _ErrorDict("vmdk file count invalid", "VMDK文件数量非法")
    PRECHECK_ERROR_DST_VM_OS_TYPE_INVALID = _ErrorDict("dst vm os type invalid", "目标云服务器操作系统类型非法")
    PRECHECK_ERROR_DST_VM_BOOT_LOADER_TYPE_INVALID = _ErrorDict("dst vm boot loader type invalid", "目标云服务器引导方式非法")
    PRECHECK_ERROR_DST_VM_BLOCK_BUS_TYPE_INVALID = _ErrorDict("dst vm block bus type invalid", "目标云服务器控制器类型非法")
    PRECHECK_ERROR_DST_VM_NET_TYPE_INVALID = _ErrorDict("dst vm net type invalid", "目标云服务器网卡类型非法")
    PRECHECK_ERROR_DST_VM_MEMORY_VALUE_INVALID = _ErrorDict("dst vm memory value invalid", "目标云服务器内存数值非法")
    PRECHECK_ERROR_DST_VM_CPU_VALUE_INVALID = _ErrorDict("dst vm cpu value invalid", "目标云服务器CPU核心数非法")
    PRECHECK_ERROR_STC_VM_NFS_PATH_EMPTY = _ErrorDict("src vm nfs path empty", "源虚拟机nas存储路径为空")

    # 导出镜像
    EXPORT_IMAGE_ERROR_COMMON = _ErrorDict("export image failed", "导出镜像失败")
    EXPORT_IMAGE_ERROR_OVA_NOT_EXISTS = _ErrorDict("ova file not exists", "OVA文件不存在")

    # 上传镜像
    UPLOAD_IMAGE_ERROR_COMMON = _ErrorDict("upload image failed", "上传镜像失败")

    # 处理镜像
    DEAL_IMAGE_ERROR_COMMON = _ErrorDict("deal image failed", "处理镜像失败")
    DEAL_IMAGE_ERROR_MF_NOT_EXISTS = _ErrorDict("mf file not exists", "MF文件不存在")
    DEAL_IMAGE_ERROR_OVF_NOT_MATCH = _ErrorDict("ovf file not match", "OVF文件不匹配")
    DEAL_IMAGE_ERROR_VMDK_NOT_MATCH = _ErrorDict("vmdk file not match", "VMDK文件不匹配")
    DEAL_IMAGE_ERROR_DISK_CONFIG_RELATE_IMAGE_PATH = _ErrorDict("disk config relate image path failed", "磁盘配置关联镜像地址失败")
    DEAL_IMAGE_ERROR_UNCOMPRESS_IMAGE_FAILED = _ErrorDict("uncompress image failed", "解压镜像失败")
    CONVERT_IMAGE_ERROR_COMMON = _ErrorDict("convert image failed", "转换镜像失败")
    CONVERT_IMAGE_ERROR_IDENTIFY_OS_DISK_FAILED = _ErrorDict("identify os disk failed", "识别系统盘失败")
    CONVERT_IMAGE_ERROR_OS_DISK_NOT_EXISTS = _ErrorDict("os disk not exists", "虚拟机系统盘不存在")
    CONVERT_IMAGE_ERROR_MULTI_OS_DISK_EXISTS = _ErrorDict("multi os disk exists", "虚拟机存在多个系统盘")

    # 创建虚拟机
    REGISTER_IMAGE_ERROR_COMMON = _ErrorDict("register image failed", "注册镜像失败")
    REGISTER_IMAGE_ERROR_UNKNOWN_VM_TYPE = _ErrorDict("unknown dst vm type", "未知的目标虚拟机类型")
    CREATE_INSTANCE_ERROR_COMMON = _ErrorDict("create instance failed", "创建虚拟机失败")
    CREATE_INSTANCE_ERROR_RUN_INSTANCE_FAILED = _ErrorDict("run instance failed", "创建虚拟机失败")
    CREATE_INSTANCE_ERROR_UPDATE_USER_QUOTAS_FAILED = _ErrorDict("update user quotas failed", "更新用户配额失败")
    CREATE_INSTANCE_ERROR_DESCRIBE_INSTANCE_FAILED = _ErrorDict("describe instance failed", "获取虚拟机详情失败")
    CREATE_INSTANCE_ERROR_START_INSTANCE_FAILED = _ErrorDict("start instance failed", "启动虚拟机失败")
    CREATE_INSTANCE_ERROR_STOP_INSTANCE_FAILED = _ErrorDict("stop instance failed", "关闭虚拟机失败")
    CREATE_INSTANCE_ERROR_CREATE_VOLUMES_FAILED = _ErrorDict("create volumes failed", "创建硬盘失败")
    CREATE_INSTANCE_ERROR_ATTACH_VOLUMES_FAILED = _ErrorDict("attach volumes failed", "加载硬盘失败")
    CREATE_INSTANCE_ERROR_COVER_IMAGES_TO_VOLUMES_FAILED = _ErrorDict("cover images to volumes failed", "覆盖硬盘数据失败")
    CREATE_INSTANCE_ERROR_UPDATE_IMAGE_STATUS_FAILED = _ErrorDict("update image status failed", "更新镜像状态失败")
    CREATE_INSTANCE_ERROR_START_INSTANCE_TIMEOUT = _ErrorDict("start instance timeout", "启动虚拟机超时")
    CREATE_INSTANCE_ERROR_STOP_INSTANCE_TIMEOUT = _ErrorDict("stop instance failed", "关闭虚拟机超时")
    CREATE_INSTANCE_ERROR_VOLUME_NOT_EXISTS = _ErrorDict("volume file not exists", "硬盘文件不存在")
    CREATE_INSTANCE_ERROR_RESTART_INSTANCE_FAILED = _ErrorDict("restart instance failed", "重启虚拟机失败")

    # 覆盖镜像
    COVER_IMAGE_ERROR_COMMON = _ErrorDict("cover image failed", "覆盖镜像失败")

    # 修复调优
    RECORRECT_AND_OPTIMIZE_ERROR_COMMON = _ErrorDict("recorrect and optimize failed", "修复调优失败")
