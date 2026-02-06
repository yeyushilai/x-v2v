# -*- coding: utf-8 -*-

import os

# 设置日志
from logger import logger

from utils.time.timex import get_current_time
from api.constants import HYPERNODE_STATUS_ACTIVE
# 暂时注释掉dlock导入，因为在当前目录结构中没有找到
# from zk.dlock import dlock


from context import WorkerContext


from constants.zk import (
    DLOCK_KEY,
    DLOCK_TIMEOUT
)

# pitrix上面的虚拟机
from constants.iaas import (
    # # 虚拟机
    # SupportInstanceType,


    # 磁盘
    SupportVolumeType,
)

from constants.common import (
    # 当前节点信息
    LOCAL_NODE_ID,
    LOCAL_NODE_IP,

    # 导出镜像
    EXPORT_IMAGE_DST_BASE_DIR,

    # 上传镜像
    UPLOAD_IMAGE_DST_BASE_DIR,

    # 转换镜像
    # DEAL_IMAGE_MOUNT_BASE_DIR,

    # 迁移相关
    MigrateStatus,
    MigratePattern
)
from constants.error import ErrorCode, ErrorMsg


from utils.common import normal_exec


# 初始化上下文
CTX = WorkerContext()

# 迁移模式映射
MIGRATE_PATTERN_MAPPER = {
    1: MigratePattern.EXPORT_IMAGE.value,
    2: MigratePattern.UPLOAD_IMAGE.value
}


# 本节点不支持调度的迁移任务（黑名单）
dispatch_task_black_list = list()

# 本节点不支持创建的虚拟机类型的会话列表
unsupported_instance_type_vm_list = list()

# 本节点不支持创建的虚拟机硬盘类型的会话列表
unsupported_volume_type_vm_list = list()

# 非法的虚拟机硬盘类型的会话列表
invalid_volume_type_vm_list = list()


def get_wait_migrate_vm_in_task(task_id):
    """获取迁移任务中等待迁移的虚拟机列表"""
    wait_migrate_status_list = MigrateStatus.list_wait_migrate_status()
    return CTX.v2v_pg.list_vm(task_id=task_id,
                              status=wait_migrate_status_list,
                              sort_key="priority")


def dispatch_task():
    """简化版：调度一个迁移任务"""
    try:
        # 尝试从数据库获取第一个迁移任务
        tasks = CTX.v2v_pg.list_migrate_task()
        if not tasks:
            logger.info("No migrate tasks available")
            return
        
        # 直接返回第一个任务
        task_info = tasks[0]
        logger.info("Dispatching task: {task_id}".format(task_id=task_info["task_id"]))
        return task_info
    except Exception as e:
        logger.error("Error dispatching task: {reason}".format(reason=str(e)))
        return


def dispatch_vm(task_info):
    """简化版：从迁移任务中调度出一个待迁移的虚拟机"""
    try:
        # 从迁移任务中调度出一个待迁移的虚拟机
        vm_session = dispatch_vm_from_task(task_info)

        if vm_session:
            # 简化：跳过资源检查
            logger.info("Skipping resource check in simplified version")
            
            # 初始化迁移虚拟机的相关信息
            vm_session = init_vm_session(task_info, vm_session)

        # 简化：跳过Redis队列更新
        logger.info("Skipping Redis queue update in simplified version")

        return vm_session
    except Exception as e:
        logger.error("Error dispatching VM: {reason}".format(reason=str(e)))
        return


def dispatch_vm_from_task(task_info):
    """简化版：从迁移任务中调度出一个待迁移的虚拟机"""
    task_id = task_info["task_id"]
    vm_info_list = get_wait_migrate_vm_in_task(task_id)

    # 取空检查
    if not vm_info_list:
        logger.info("there is not wait migrate vm in task, task id: "
                    "{task_id}".format(task_id=task_id))
        return

    # 简化：直接返回第一个虚拟机，跳过复杂的资源检查
    vm_info = vm_info_list[0]
    session_id = vm_info["session_id"]
    
    logger.info("Dispatching VM: {session_id} from task: {task_id}"
                .format(session_id=session_id, task_id=task_id))
    return vm_info


def reset_unsupported_instance_type_vms():
    """重置不支持虚拟机类型的迁移项"""
    detail_status = dict(status=MigrateStatus.FAILED.value,
                         end_time=get_current_time())

    err_code = ErrorCode.ERROR_DST_VM_TYPE_INVALID.value
    err_msg = ErrorMsg.ERROR_DST_VM_TYPE_INVALID.value
    detail_status["err_msg"] = err_msg.zh
    detail_status["err_code"] = err_code
    for session_id in unsupported_instance_type_vm_list:
        CTX.v2v_pg.update_vm(session_id=session_id, columns=detail_status)
        logger.info("reset vm session to failed successfully, session id: "
                    "{session_id}, err code: {err_code}, err msg: {err_msg}"
                    "".format(session_id=session_id,
                              err_msg=err_msg.en,
                              err_code=err_code))


def reset_unsupported_volume_type_vms(vm_list):
    """重置不支持硬盘类型的迁移项"""
    detail_status = dict(status=MigrateStatus.FAILED.value,
                         end_time=get_current_time())

    err_code = ErrorCode.ERROR_DST_VM_VOLUME_TYPE_INVALID.value
    err_msg = ErrorMsg.ERROR_DST_VM_VOLUME_TYPE_INVALID.value
    detail_status["err_msg"] = err_msg.zh
    detail_status["err_code"] = err_code
    for session_id in vm_list:
        CTX.v2v_pg.update_vm(session_id=session_id, columns=detail_status)
        logger.info("reset vm session to failed successfully, session id: "
                    "{session_id}, err code: {err_code}, err msg: {err_msg}"
                    "".format(session_id=session_id,
                              err_msg=err_msg.en,
                              err_code=err_code))


def check_local_node_resource(vm_session):
    """判断当前节点是否有空闲的硬件资源"""

    bot_set = CTX.iaas.describe_bots(hyper_ids=[LOCAL_NODE_ID],
                                     zone=CTX.local_node.zone_id)
    session_id = vm_session["session_id"]

    # 检查状态
    hyper_status = bot_set.get("status")
    if hyper_status != HYPERNODE_STATUS_ACTIVE:
        err_msg = "the status of hyper node is invalid, node id: {node_id}, " \
                  "status: {status}" \
                  "".format(node_id=LOCAL_NODE_ID, status=hyper_status)
        logger.error(err_msg)
        return False

    # 检查CPU
    dst_vm_cpu_core = vm_session["dst_vm_cpu_core"]
    free_cpu_core = bot_set["free_vcpu"]
    if dst_vm_cpu_core > free_cpu_core:
        log_msg = "cpu core out of limit, session id: {session_id}, " \
                  "dst vm cpu core: {dst_vm_cpu_core}, " \
                  "free cpu core: {free_cpu_core}" \
                  "".format(session_id=session_id,
                            dst_vm_cpu_core=dst_vm_cpu_core,
                            free_cpu_core=free_cpu_core)
        logger.info(log_msg)
        return False

    # 检查内存
    dst_vm_memory = vm_session["dst_vm_memory"]
    free_memory = bot_set["free_memory"]
    if dst_vm_memory / 1024 > free_memory:
        log_msg = "memory out of limit, session id: {session_id}, " \
                  "dst vm memory: {dst_vm_memory}, " \
                  "free memory: {free_memory}" \
                  "".format(session_id=session_id,
                            dst_vm_memory=dst_vm_memory / 1024,
                            free_memory=free_memory)
        logger.info(log_msg)
        return False

    # 检查磁盘
    dst_vm_disk = vm_session["dst_vm_disk"]
    free_disk = bot_set.get("free_disk")
    vm_disk_size = 0
    for disk in dst_vm_disk:
        vm_disk_size += disk.get("size")
    if vm_disk_size > free_disk:
        log_msg = "disk size out of limit, session id: {session_id}, " \
                  "vm disk size: {vm_disk_size}, " \
                  "free disk: {free_disk}" \
                  "".format(session_id=session_id,
                            vm_disk_size=vm_disk_size,
                            free_disk=free_disk)
        logger.info(log_msg)
        return False

    return True


def init_vm_session(task_info, vm_session):
    """初始化迁移虚拟机的
    1.初始化目录
    2.更新相关信息到内存和v2v数据库
    """
    session_id = vm_session["session_id"]

    # 1.初始化目录
    logger.info("init directory, session id: {session_id}"
                "".format(session_id=session_id))
    vm_session["extra"] = dict()
    task_pattern = MIGRATE_PATTERN_MAPPER[task_info["task_pattern"]]
    if task_pattern == MigratePattern.EXPORT_IMAGE.value:
        export_dir = os.path.join(EXPORT_IMAGE_DST_BASE_DIR, session_id)
        if not os.path.isdir(export_dir):
            normal_exec("mkdir -p %s" % export_dir)
        vm_session["extra"]["export_dir"] = export_dir

    elif task_pattern == MigratePattern.UPLOAD_IMAGE.value:
        upload_dir = os.path.join(UPLOAD_IMAGE_DST_BASE_DIR, session_id)
        if not os.path.isdir(upload_dir):
            normal_exec("mkdir -p %s" % upload_dir)
        vm_session["extra"]["upload_dir"] = upload_dir

    # 2.更新相关信息到内存和v2v数据库
    running = MigrateStatus.RUNNING.value
    current_time = get_current_time()
    columns = dict(status=running,
                   indeed_dst_node_id=LOCAL_NODE_ID,
                   indeed_dst_node_ip=LOCAL_NODE_IP,
                   start_time=current_time)
    logger.info("init vm session, session id: {session_id}, src "
                "status: {src_status}, dst status: {dst_status}, "
                "start time: {start_time}"
                .format(session_id=session_id, src_status=vm_session["status"],
                        dst_status=running, start_time=current_time))
    vm_session.update(columns)
    CTX.v2v_pg.update_vm(session_id=session_id, columns=columns)

    return vm_session


def update_relative_queue_task(task_info):
    """更新redis中队列中对应的任务
    判断逻辑：若任务中的没有待迁移的虚拟机，则将任务ID从redis的数据结构中移除
    """
    task_id = task_info["task_id"]
    vm_list = get_wait_migrate_vm_in_task(task_id)
    if vm_list:
        return

    CTX.redis.remove_define_node_define_task(LOCAL_NODE_ID, task_id)
    CTX.redis.remove_auto_node_define_task(task_id)
    logger.info("there is not wait migrate vm in task, has removed "
                "task id from redis, task id: {task_id}"
                .format(task_id=task_id))
