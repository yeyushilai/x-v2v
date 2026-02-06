#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

# 设置日志
from logger import logger

from utils.time.timex import get_current_time
from api.constants import HYPERNODE_STATUS_ACTIVE

from worker import Worker
from context import WorkerContext
from dispatcher import dispatch_task, dispatch_vm


from constants.common import (
    # 当前节点信息
    LOCAL_NODE_ID,

    # 自身
    MAX_MIGRATING_NUM,
    DATA_DIR,

    # 调试
    CONCURRENCY_MIGRATE,

    # 迁移全局
    INDEED_START_MIGRATE_TIMEOUT,
    INDEED_END_MIGRATE_TIMEOUT,

    # 导出镜像
    EXPORT_IMAGE_DST_BASE_DIR,
    EXPORT_IMAGE_LOG_PATH,

    # 上传镜像
    UPLOAD_IMAGE_DST_BASE_DIR,

    # 转换镜像
    # DEAL_IMAGE_MOUNT_BASE_DIR,
    # DEAL_IMAGE_FILE_LOCK_BASE_DIR,

    # 迁移相关
    MigrateStatus,
    WorkerAction
)
from constants.error import ErrorCode, ErrorMsg

# 初始化上下文
ctx = WorkerContext()


def check_hyper_node():
    # 简化检查，只确保能够获取节点信息
    try:
        bot_set = ctx.iaas.describe_bots(hyper_ids=[LOCAL_NODE_ID],
                                         zone=ctx.local_node.zone_id)
        logger.info("Hyper node checked successfully")
    except Exception as e:
        err_msg = "Failed to check hyper node: {reason}".format(reason=str(e))
        logger.error(err_msg)
        raise Exception(err_msg)


def init_directory():
    """初始化目录"""

    # V2V项目的基准目录
    # eg: /pitrix/data/v2v
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    # 导出镜像时，若相关的日志所在的目录未生成，需要生成
    export_image_log_base_dir = os.path.dirname(EXPORT_IMAGE_LOG_PATH)
    if not os.path.isdir(export_image_log_base_dir):
        os.mkdir(export_image_log_base_dir)

    # 导出镜像时，临时保存镜像的基准目录
    # eg: /pitrix/data/v2v/v2v_export
    if not os.path.isdir(EXPORT_IMAGE_DST_BASE_DIR):
        os.mkdir(EXPORT_IMAGE_DST_BASE_DIR)

    # 上传镜像时，临时保存镜像的基准目录
    # eg: /pitrix/data/v2v/v2v_upload
    if not os.path.isdir(UPLOAD_IMAGE_DST_BASE_DIR):
        os.mkdir(UPLOAD_IMAGE_DST_BASE_DIR)


def register_hyper_node():
    """简化版：跳过ZooKeeper注册"""
    logger.info("Skipping ZooKeeper registration in simplified version")


def reset_remained_vms():
    """简化版：跳过残余虚拟机重置"""
    logger.info("Skipping remained VMs reset in simplified version")


def supervise_worker(v2v_worker):
    """简化版：监管worker状态"""
    alive_threads = v2v_worker.alive_threads
    if alive_threads:
        logger.info("Supervising %d alive worker threads" % len(alive_threads))
    else:
        logger.info("No alive worker threads to supervise")


def check_local_node_queue():
    """简化版：判断当前节点是否有空闲的队列"""
    # 直接返回True，假设节点总是有空闲队列
    logger.info("Checking local node queue: assuming available")
    return True


def loop():
    """循环调度任务，调度待迁移主机、执行迁移"""
    action = WorkerAction.IMMEDIATELY_MIGRATE.value
    v2v_worker = Worker(CONCURRENCY_MIGRATE)

    while True:
        try:
            # 监管当前worker的状态
            supervise_worker(v2v_worker)

            # 判断当前节点是否有空闲的队列
            check_local_node_queue()

            # 调度一个迁移任务
            task_info = dispatch_task()
            if not task_info:
                logger.info("dispatch a suitable task failed, sleep 30s")
                time.sleep(30)
                continue

            # 从迁移任务中调度出一个待迁移的虚拟机
            vm_session = dispatch_vm(task_info)
            if not vm_session:
                logger.info("dispatch a suitable vm failed, task id: {task_id}"
                            ", sleep 30s"
                            "".format(task_id=task_info["task_id"]))
                time.sleep(30)
                continue

            # 执行迁移动作
            v2v_worker.start(action, vm_session)
            logger.info("dispatch a suitable vm and send migrate request "
                        "successfully, session id: {session_id}, "
                        "task id: {task_id}"
                        "".format(session_id=vm_session["session_id"],
                                  task_id=task_info["task_id"]))

        except Exception as e:
            log_msg = "dispatch a suitable vm and send migrate request failed," \
                      " sleep 30s, error reason: {reason}" \
                      "".format(reason=str(e))
            logger.exception(log_msg)
            time.sleep(30)

        finally:
            logger.info("sleep 5s")
            time.sleep(5)


def main():

    # 初始化目录
    init_directory()

    # 自检hyper节点
    check_hyper_node()

    # 注册hyper节点
    register_hyper_node()

    # 重置残留的关联虚拟机
    reset_remained_vms()

    # 循环调度任务，调度待迁移主机、执行迁移
    loop()


if __name__ == '__main__':
    main()
