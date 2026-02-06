# -*- coding: utf-8 -*-

"""
功能：统一异常处理模块
"""

from logger import logger
from constants.error import ErrorCode, ErrorMsg


class V2VMigrationError(Exception):
    """
    V2V迁移异常基类
    """

    def __init__(self, message, error_code=None, error_msg=None):
        self.message = message
        self.error_code = error_code or ErrorCode.ERROR_COMMON.value
        self.error_msg = error_msg or ErrorMsg.ERROR_COMMON.value
        super(V2VMigrationError, self).__init__(self.message)


class ExportImageError(V2VMigrationError):
    """
    导出镜像异常
    """

    def __init__(self, message):
        super(ExportImageError, self).__init__(
            message,
            error_code=ErrorCode.EXPORT_IMAGE_ERROR_COMMON.value,
            error_msg=ErrorMsg.EXPORT_IMAGE_ERROR_COMMON.value
        )


class DealImageError(V2VMigrationError):
    """
    处理镜像异常
    """

    def __init__(self, message):
        super(DealImageError, self).__init__(
            message,
            error_code=ErrorCode.DEAL_IMAGE_ERROR_COMMON.value,
            error_msg=ErrorMsg.DEAL_IMAGE_ERROR_COMMON.value
        )


class UploadImageError(V2VMigrationError):
    """
    上传镜像异常
    """

    def __init__(self, message):
        super(UploadImageError, self).__init__(
            message,
            error_code=ErrorCode.UPLOAD_IMAGE_ERROR_COMMON.value,
            error_msg=ErrorMsg.UPLOAD_IMAGE_ERROR_COMMON.value
        )


class CreateVMError(V2VMigrationError):
    """
    创建虚拟机异常
    """

    def __init__(self, message):
        super(CreateVMError, self).__init__(
            message,
            error_code=ErrorCode.CREATE_INSTANCE_ERROR_COMMON.value,
            error_msg=ErrorMsg.CREATE_INSTANCE_ERROR_COMMON.value
        )


class FixTuneError(V2VMigrationError):
    """
    修复调优异常
    """

    def __init__(self, message):
        super(FixTuneError, self).__init__(
            message,
            error_code=ErrorCode.RECORRECT_AND_OPTIMIZE_ERROR_COMMON.value,
            error_msg=ErrorMsg.RECORRECT_AND_OPTIMIZE_ERROR_COMMON.value
        )


def handle_exception(func):
    """
    异常处理装饰器
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except V2VMigrationError as e:
            logger.error("V2V migration error: {message}, error code: {code}".format(
                message=e.message,
                code=e.error_code
            ))
            # 这里可以根据需要添加额外的处理逻辑
            raise
        except Exception as e:
            logger.error("Unexpected error: {message}".format(message=str(e)))
            # 将普通异常包装为V2VMigrationError
            raise V2VMigrationError(str(e))

    return wrapper


def handle_migration_exception(vm_session):
    """
    迁移异常处理函数
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except V2VMigrationError as e:
                logger.error("Migration error: {message}, error code: {code}".format(
                    message=e.message,
                    code=e.error_code
                ))
                # 更新虚拟机状态为失败
                vm_session.update_detail_migrate_status({
                    "status": "FAILED",
                    "err_msg": e.message,
                    "err_code": e.error_code
                })
                return False
            except Exception as e:
                logger.error("Unexpected migration error: {message}".format(message=str(e)))
                # 更新虚拟机状态为失败
                vm_session.update_detail_migrate_status({
                    "status": "FAILED",
                    "err_msg": str(e),
                    "err_code": ErrorCode.ERROR_COMMON.value
                })
                return False

        return wrapper

    return decorator
