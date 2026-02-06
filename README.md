# V2V 虚拟机迁移工具

## 项目简介

V2V (Virtual to Virtual) 是一个支持跨虚拟化平台迁移虚拟机的工具，提供导出和上传镜像等多种迁移方式。

## 项目结构

```
v2v/
├── constants/           # 常量定义
├── misc/                # 杂项文件
├── platforms/           # 平台接口
│   ├── iaas/            # IAAS平台接口
│   ├── nas/             # NAS存储接口
│   └── vmware_vsphere/  # VMware vSphere平台接口
├── storage/             # 存储相关工具
│   ├── nbd/             # NBD相关工具
│   └── qbd/             # QBD相关工具
├── infra/               # 基础设施工具
│   ├── pg/              # PostgreSQL相关工具
│   ├── redis/           # Redis相关工具
│   └── zk/              # ZooKeeper相关工具
├── utils/               # 工具类
│   ├── common/          # 通用工具
│   ├── config/          # 配置工具
│   ├── convert/         # 转换工具
│   └── time/            # 时间工具
├── logger.py            # 日志模块
├── main.py              # 主入口
├── dispatcher.py        # 任务调度器
├── migration.py         # 迁移核心逻辑
├── vm.py                # 虚拟机会话类
├── handler.py           # 任务处理器
├── checker.py           # 迁移检查器
└── hyper_node.py        #  Hyper节点类
```

## 核心功能

1. **导出镜像**：从源虚拟机导出镜像文件
2. **上传镜像**：上传本地镜像文件到目标平台
3. **处理镜像**：解压、检查、转换镜像格式
4. **创建虚拟机**：在目标平台创建虚拟机
5. **覆盖镜像**：将迁移的镜像覆盖到目标虚拟机
6. **修复调优**：修复目标虚拟机的驱动问题并进行优化

## 安装和依赖

### 依赖项

- Python 3.x
- xxxcloud.iaas (xxxcloud云平台API)
- 其他必要的Python库

### 安装方法

1. 克隆代码库
2. 安装依赖项
3. 配置相关参数

## 使用方法

### 运行迁移服务

```bash
python main.py
```

### 迁移流程

1. **任务调度**：`dispatcher.py` 从队列中获取迁移任务
2. **虚拟机调度**：从任务中选择一个待迁移的虚拟机
3. **迁移执行**：`migration.py` 执行具体的迁移操作
4. **状态更新**：更新虚拟机的迁移状态
5. **清理**：清理临时文件和目录

## 代码结构

### 核心类

- **BaseMigration**：迁移基类，定义了迁移的基本流程
- **VMSession**：虚拟机会话类，管理虚拟机的状态和配置
- **WorkerContext**：工作上下文类，管理各种服务的实例
- **MigrateHandler**：迁移处理器，处理具体的迁移任务

### 迁移流程

1. **导出/上传镜像**：从源平台获取镜像
2. **处理镜像**：转换镜像格式，生成目标虚拟机磁盘信息
3. **创建虚拟机**：在目标平台创建虚拟机
4. **覆盖镜像**：将迁移的镜像覆盖到目标虚拟机
5. **修复调优**：修复驱动问题并进行优化

## 日志系统

本项目使用自定义的日志系统，配置如下：

- **日志文件**：`logs/v2v_migration_YYYYMMDD.log`
- **日志格式**：`%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **日志级别**：INFO

### 使用方法

```python
from logger import logger

logger.info("Info message")
logger.error("Error message")
```

## 注意事项

1. **依赖问题**：运行前确保所有必要的依赖都已安装
2. **权限问题**：确保执行用户有足够的权限进行文件操作和系统调用
3. **网络问题**：迁移过程中需要稳定的网络连接
4. **存储空间**：确保有足够的存储空间用于存储镜像文件
5. **源虚拟机状态**：迁移前确保源虚拟机处于关机状态

## 版本历史

- 初始版本：基本功能实现
- 优化版本：移除多余权限校验代码，优化日志系统，简化迁移流程

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

[MIT License](LICENSE)

