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

### 使用 uv 管理工具（推荐）

本项目使用 [uv](https://github.com/astral-sh/uv) 作为Python包管理工具，它是一个快速的Python包安装程序和解析器，可以替代pip和pip-tools。

#### 安装 uv

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 初始化项目

首次使用时，项目已经初始化了uv配置，包含以下内容：

- `pyproject.toml` - 项目配置文件
- `.venv/` - 虚拟环境目录（首次运行 `uv sync` 后创建）

#### 创建和激活虚拟环境

1. **同步依赖并创建虚拟环境**：
```bash
uv sync
```

这将创建虚拟环境并安装所有必要的依赖。

2. **激活虚拟环境**：

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

#### 安装开发依赖

如果需要运行测试或进行代码检查，安装开发依赖：

```bash
uv sync --extra dev
```

#### 运行项目

在虚拟环境中运行项目：

```bash
uv run python main.py
```

或者先激活虚拟环境，然后直接运行：

```bash
python main.py
```

#### 运行测试

```bash
uv run pytest
```

或者：

```bash
pytest
```

#### 代码检查

```bash
uv run flake8
```

或者：

```bash
flake8
```

#### 添加新依赖

添加生产环境依赖：
```bash
uv add package_name
```

添加开发环境依赖：
```bash
uv add --dev package_name
```

#### 更新依赖

```bash
uv lock --upgrade
uv sync
```

### 传统安装方法

如果不想使用uv，可以使用传统的pip安装方式：

1. 创建虚拟环境：
```bash
python -m venv .venv
```

2. 激活虚拟环境（参考上面的激活命令）

3. 安装依赖：
```bash
pip install pyyaml>=6.0 pyvmomi>=8.0.0 pycryptodome>=3.15.0
```

### 依赖项

- Python == 3.11
- pyyaml >= 6.0 - YAML文件解析
- pyvmomi >= 8.0.0 - VMware vSphere API
- pycryptodome >= 3.15.0 - 加密库
- pytest >= 7.0.0 - 测试框架（开发依赖）
- flake8 >= 5.0.0 - 代码检查工具（开发依赖）

### 配置文件

1. **配置文件路径**：`/pitrix/conf/v2v_worker.yaml`
2. **如果配置文件不存在**，系统将使用默认配置值

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



## 许可证

[MIT License](LICENSE)

## 提交 Issue

如果您在使用过程中遇到问题，或有新的功能建议，欢迎在 GitHub 上提交 Issue：

1. 访问项目的 GitHub 仓库页面
2. 点击 "Issues" 选项卡
3. 点击 "New issue" 按钮
4. 选择适当的 issue 模板（如果有）
5. 填写 issue 标题和详细描述
6. 点击 "Submit new issue" 按钮提交

### Issue 提交建议

- **问题报告**：
  - 描述您遇到的具体问题
  - 提供重现步骤
  - 说明您期望的行为
  - 附上相关的错误信息或日志
  - 注明您的环境信息（Python 版本、操作系统等）

- **功能请求**：
  - 描述您希望添加的功能
  - 说明为什么这个功能是有用的
  - 如有可能，提供功能实现的建议

我们会定期查看并处理提交的 Issue，感谢您对项目的贡献！
