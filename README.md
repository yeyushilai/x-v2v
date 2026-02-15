# X-V2V - 虚拟机迁移工具

x-v2v 是一个支持跨虚拟化平台迁移虚拟机的工具，提供导出和上传镜像等多种迁移方式。

## 功能特性

- **导出镜像迁移**：支持从 VMware 平台导出虚拟机镜像
- **上传镜像迁移**：支持将镜像上传到目标平台
- **多磁盘支持**：支持系统盘和多个数据盘的迁移
- **网络配置**：支持源虚拟机网络信息的保留和迁移
- **日志管理**：详细的迁移日志记录和追踪
- **配置灵活**：通过 YAML 配置文件灵活配置各项参数

## 项目结构

```
x-v2v/
├── clients/           # 客户端工具
│   ├── cmd_cli.py     # 命令行客户端
│   └── nfs_cli.py     # NFS 客户端
├── constants/         # 常量定义
│   ├── enum.py        # 枚举类型
│   └── template.py    # 模板定义
├── core/              # 核心模块
│   ├── config.py      # 配置管理
│   └── logger.py      # 日志管理
├── statics/           # 静态资源
│   └── template.lz4   # 实例模板
├── tools/             # 工具模块
│   ├── convert_tool.py # 转换工具
│   ├── dict_tool.py   # 字典工具
│   ├── file_tool.py   # 文件工具
│   └── time_tool.py   # 时间工具
├── config.yaml        # 配置文件
├── main.py            # 主程序入口
├── vm_session.py      # 虚拟机会话管理
├── migration.py       # 迁移核心逻辑
├── pyproject.toml     # 项目依赖配置
├── uv_manager.py      # UV 项目管理工具
└── setup_uv.py        # UV 环境设置脚本
```

## 安装说明

### 环境要求

- Python 3.9+
- 依赖：loguru、pyyaml、xmltodict


## 配置说明

主要配置在 `config.yaml` 文件中，包含以下部分：

- `project` - 项目基本信息
- `self` - 本地路径配置
- `setting` - 迁移设置
- `migration` - 迁移详细参数
- `hyper` - 虚拟化平台配置
- `vmware_vsphere` - VMware 配置
- `redis` - Redis 配置
- `zk` - ZooKeeper 配置
- `nfs` - NFS 配置
- `log` - 日志配置

## 使用方法

### 运行示例

```bash
python main.py
```

## 迁移流程

1. **准备阶段**：检查源虚拟机状态，准备迁移参数
2. **导出阶段**：从 VMware 导出虚拟机镜像（使用 OVF Tool）
3. **转换阶段**：将 VMDK 格式转换为 QCOW2 格式（使用 qemu-img）
4. **上传阶段**：上传镜像到目标平台
5. **创建实例**：在目标平台创建新的虚拟机实例
6. **完成验证**：验证迁移结果，更新迁移状态

## 许可证

本项目使用 LICENSE 文件中指定的许可证。
