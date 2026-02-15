# -*- coding: utf-8 -*-

"""功能：枚举定义"""

from enum import Enum


class DescribedEnum(Enum):
    """
    可描述的枚举类基建
    mark: int        唯一标识
    desc: str        描述信息
    """

    def __init__(self, *args):
        pass

    @property
    def mark(self):
        return self.value

    @property
    def desc(self):
        return str(self.value)

    @classmethod
    def get_all_marks(cls) -> list[int]:
        return [described_enum.mark for described_enum in cls]

    @classmethod
    def get_all_descs(cls) -> list[str]:
        return [described_enum.desc for described_enum in cls]

    @classmethod
    def get_choices(cls):
        return ((described_enum.mark, described_enum.desc) for described_enum in cls)


class VmwarevSphereNotConnectReason(DescribedEnum):
    """Vmware vSphere 平台无法连接的原因"""

    NET_ERROR = "net_error"
    COMMON_ERROR = "common_error"


class VmwarevSphereVmStatus(DescribedEnum):
    """Vmware vSphere 平台虚拟机状态枚举"""

    POWEREDON = "poweredOn"
    POWEREDOFF = "poweredOff"
    SUSPENDED = "suspended"


class QemuImgAction(Enum):
    """QemuImg动作"""
    CONVERT = "convert"

class WorkerAction(DescribedEnum):
    """worker动作"""

    IMMEDIATELY_MIGRATE = "immediately_migrate"  # 立即执行
    TIME_MIGRATE = "time_migrate"  # 定时执行


class MigratePattern(DescribedEnum):
    """迁移模式"""

    EXPORT_IMAGE = "export_image"  # 导出镜像
    UPLOAD_IMAGE = "upload_image"  # 上传镜像


class MigrateStep(DescribedEnum):
    """迁移步骤"""

    EXPORT_IMAGE = "export_image"  # 导出镜像
    UPLOAD_IMAGE = "upload_image"  # 上传镜像
    DEAL_IMAGE = "deal_image"  # 处理镜像
    CREATE_INSTANCE = "create_instance"  # 创建虚拟机
    COVER_IMAGE = "cover_image"  # 覆盖镜像
    RECORRECT_AND_OPTIMIZE = "recorrect_and_optimize"  # 修复调优


class MigrateProcess(DescribedEnum):
    """迁移进度"""

    # 导出镜像
    START_EXPORT_IMAGE_PROCESS = 5  # 开始导出镜像进度
    END_EXPORT_IMAGE_PROCESS = 25  # 结束导出镜像进度

    # 上传镜像
    START_UPLOAD_IMAGE_PROCESS = 5  # 开始上传镜像进度
    END_UPLOAD_IMAGE_PROCESS = 25  # 结束上传镜像进度

    # 处理镜像
    START_DEAL_IMAGE_PROCESS = 30  # 开始处理镜像进度
    END_DEAL_IMAGE_PROCESS = 50  # 结束处理镜像进度

    # 创建虚拟机
    START_CREATE_INSTANCE_PROCESS = 55  # 开始创建虚拟机进度
    END_CREATE_INSTANCE_PROCESS = 70  # 结束创建虚拟机进度

    # 覆盖镜像
    START_COVER_IMAGE_PROCESS = 75  # 开始覆盖镜像进度
    END_COVER_IMAGE_PROCESS = 90  # 结束覆盖镜像进度

    # 修复调优
    START_RECORRECT_AND_OPTIMIZE_PROCESS = 95  # 开始修复调优进度
    END_RECORRECT_AND_OPTIMIZE_PROCESS = 100  # 结束修复调优进度


class MigrateStatus(DescribedEnum):
    """迁移状态"""

    READY = "ready"                                     # 就绪
    QUEUING = "queuing"                                 # 排队中
    PENDING = "pending"                                 # 重试排队中
    RUNNING = "running"                                 # 运行中
    COMPLETED = "completed"                             # 已完成
    FAILED = "failed"                                   # 失败

    @classmethod
    def list_wait_migrate_status(cls):
        """等待迁移的的状态列表"""
        return [cls.QUEUING.value, cls.PENDING.value]

    @classmethod
    def list_end_migrate_status(cls):
        """处于终态的状态列表"""
        return [cls.COMPLETED.value, cls.FAILED.value]


class RunningDetailMigrateStatus(DescribedEnum):
    """迁移中时详细的子步骤进度和状态"""

    # 开始导出镜像时的详细状态
    START_EXPORT_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.EXPORT_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.START_EXPORT_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束导出镜像时的详细状态
    END_EXPORT_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.EXPORT_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.END_EXPORT_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 开始上传镜像时的详细状态
    START_UPLOAD_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.UPLOAD_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.START_UPLOAD_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束上传镜像时的详细状态
    END_UPLOAD_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.UPLOAD_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.END_UPLOAD_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 开始处理镜像时的详细状态
    START_DEAL_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.DEAL_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.START_DEAL_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束处理镜像时的详细状态
    END_DEAL_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.DEAL_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.END_DEAL_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 开始创建虚拟机时的详细状态
    START_CREATE_INSTANCE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.CREATE_INSTANCE.value, err_msg="", err_code=0),
        process=MigrateProcess.START_CREATE_INSTANCE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束创建虚拟机时的详细状态
    END_CREATE_INSTANCE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.CREATE_INSTANCE.value, err_msg="", err_code=0),
        process=MigrateProcess.END_CREATE_INSTANCE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 开始覆盖镜像时的详细状态
    START_COVER_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.COVER_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.START_COVER_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束覆盖镜像时的详细状态
    END_COVER_IMAGE_DETAIL_STATUS = dict(
        step=dict(step=MigrateStep.COVER_IMAGE.value, err_msg="", err_code=0),
        process=MigrateProcess.END_COVER_IMAGE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 开始修复调优时的详细状态
    START_RECORRECT_AND_OPTIMIZE_DETAIL_STATUS = dict(
        step=dict(
            step=MigrateStep.RECORRECT_AND_OPTIMIZE.value, err_msg="", err_code=0
        ),
        process=MigrateProcess.START_RECORRECT_AND_OPTIMIZE_PROCESS.value,
        status=MigrateStatus.RUNNING.value,
    )

    # 结束修复调优时的详细状态
    END_RECORRECT_AND_OPTIMIZE_DETAIL_STATUS = dict(
        step=dict(
            step=MigrateStep.RECORRECT_AND_OPTIMIZE.value, err_msg="", err_code=0
        ),
        process=MigrateProcess.END_RECORRECT_AND_OPTIMIZE_PROCESS.value,
        status=MigrateStatus.COMPLETED.value,
    )
