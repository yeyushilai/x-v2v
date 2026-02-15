# -*- coding: utf-8 -*-

import os
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
import yaml


@dataclass
class ProjectConfig:
    name: str = "x-v2v"
    version: str = "1.0.0"


@dataclass
class MigrationConfig:
    indeed_start_migrate_timeout: int = 300
    indeed_end_migrate_timeout: int = 86400
    
    export_image_log_path: str = "/x-v2v/log/ovftool.log"
    export_image_log_level: str = "warning"
    export_image_log_to_console: str = ""
    export_image_dst_base_dir: str = "v2v_export"
    export_image_dst_format_ova: str = "ova"
    export_image_timeout: int = 86400
    export_image_max_retry_times: int = 5
    export_image_cmd_vi_prefix: str = "vi://"
    export_image_cmd_nosslverify: str = "--noSSLVerify"
    export_image_cmd_overwrite: str = "--overwrite"
    export_image_cmd_machineoutput: str = "--machineOutput"
    export_image_cmd_quiet: str = "--quiet"
    export_image_cmd_noimagefiles: str = "--noImageFiles"
    export_image_cmd_poweroffsource: str = "--powerOffSource"
    export_image_cmd_nonvramfile: str = "--noNvramFile"
    export_image_cmd_acceptalleulas: str = "--acceptAllEulas"
    
    upload_image_ld_nfs_so_path: str = "/x-v2v/iaas/lib/ld_nfs.so"
    upload_image_dst_base_dir: str = "v2v_upload"
    upload_image_timeout: int = 86400
    
    deal_image_src_format_vmdk: str = "vmdk"
    deal_image_dst_format_qcow2: str = "qcow2"
    deal_image_convert_image_timeout: int = 86400
    deal_image_mount_base_dir: str = "v2v_mount"
    deal_image_file_lock_base_dir: str = "v2v_lock"
    
    create_instance_image_file_path: str = "template.lz4"
    create_instance_run_instance_timeout: int = 1800
    create_instance_start_instance_timeout: int = 1200
    create_instance_restart_instance_timeout: int = 1200
    create_instance_stop_instance_timeout: int = 1200
    create_instance_create_volumes_timeout: int = 1200
    create_instance_attach_volumes_timeout: int = 600
    
    cover_image_timeout: int = 86400


@dataclass
class HyperConfig:
    image_base_dir: str = "/data/images"
    vmware_ovf_tool_path: str = "/usr/bin/ovftool"
    qemu_img_tool_path: str = "/usr/bin/qemu-img"
    container_mode: str = "local"


@dataclass
class SeedConfig:
    nodes: List[str] = field(default_factory=lambda: ["192.168.1.100"])
    image_repository_base_dir: str = "/data/repository"
    id_rsa_path: str = "/root/.ssh/id_rsa"
    default_user: str = "root"


@dataclass
class RedisConfig:
    host: str = "127.0.0.1"
    port: int = 6379
    password: str = ""
    db: int = 0
    max_connections: int = 10
    conf_name_v2v: str = "x-v2v"
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    max_connection_number: int = 1000
    key_prefix: str = "v2v_"
    key_suffix_auto_node: str = "auto"


@dataclass
class ZKConfig:
    hosts: List[str] = field(default_factory=lambda: ["127.0.0.1:2181"])
    timeout: int = 30000
    x_v2v_zk_base_dir: str = "/x-v2v"
    dlock_key: str = "x-v2v"
    dlock_timeout: int = 5


@dataclass
class NFSConfig:
    mount_point: str = "/mnt/nfs"
    server: str = "192.168.1.200"
    export_path: str = "/export/x-v2v"


@dataclass
class LogConfig:
    level: str = "INFO"
    log_dir: str = "/var/log/x-v2v"
    max_bytes: int = 10485760
    backup_count: int = 5


@dataclass
class VmwareVsphereConfig:
    timeout_connect_to_vmware_vsphere: int = 200


@dataclass
class SelfConfig:
    data_dir: str = "/x-v2v/iaas/data"
    deploy_dir: str = "/x-v2v/iaas/deploy"


@dataclass
class SettingConfig:
    concurrency_migrate: int = 3
    max_migrating_num: int = 10
    clean_after_failed: bool = True
    vm_max_migrate_timeout: int = 86400


@dataclass
class ResourceConfig:
    ld_nfs_so: str = "/x-v2v/iaas/lib/ld_nfs.so"


class Config:
    _instance: Optional['Config'] = None
    _config_data: Dict[str, Any] = {}
    _config_path: Optional[str] = None
    
    _project: Optional[ProjectConfig] = None
    _migration: Optional[MigrationConfig] = None
    _hyper: Optional[HyperConfig] = None
    _seed: Optional[SeedConfig] = None
    _redis: Optional[RedisConfig] = None
    _zk: Optional[ZKConfig] = None
    _nfs: Optional[NFSConfig] = None
    _log: Optional[LogConfig] = None
    _self: Optional[SelfConfig] = None
    _setting: Optional[SettingConfig] = None
    _resource: Optional[ResourceConfig] = None
    _vmware_vsphere: Optional[VmwareVsphereConfig] = None

    def __new__(cls, config_path: Optional[str] = None) -> 'Config':
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path: Optional[str] = None) -> None:
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config.yaml'
            )
        
        self._config_path = config_path
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config_data = yaml.safe_load(f) or {}
        
        self._parse_config()

    def _parse_config(self) -> None:
        project_data = self._config_data.get('project', {})
        self._project = ProjectConfig(
            name=project_data.get('name', 'x-v2v'),
            version=project_data.get('version', '1.0.0')
        )
        
        migration_data = self._config_data.get('migration', {})
        self._migration = MigrationConfig(
            indeed_start_migrate_timeout=migration_data.get('indeed_start_migrate_timeout', 300),
            indeed_end_migrate_timeout=migration_data.get('indeed_end_migrate_timeout', 86400),
            
            export_image_log_path=migration_data.get('export_image_log_path', '/x-v2v/log/ovftool.log'),
            export_image_log_level=migration_data.get('export_image_log_level', 'warning'),
            export_image_log_to_console=migration_data.get('export_image_log_to_console', ''),
            export_image_dst_base_dir=migration_data.get('export_image_dst_base_dir', 'v2v_export'),
            export_image_dst_format_ova=migration_data.get('export_image_dst_format_ova', 'ova'),
            export_image_timeout=migration_data.get('export_image_timeout', 86400),
            export_image_max_retry_times=migration_data.get('export_image_max_retry_times', 5),
            export_image_cmd_vi_prefix=migration_data.get('export_image_cmd_vi_prefix', 'vi://'),
            export_image_cmd_nosslverify=migration_data.get('export_image_cmd_nosslverify', '--noSSLVerify'),
            export_image_cmd_overwrite=migration_data.get('export_image_cmd_overwrite', '--overwrite'),
            export_image_cmd_machineoutput=migration_data.get('export_image_cmd_machineoutput', '--machineOutput'),
            export_image_cmd_quiet=migration_data.get('export_image_cmd_quiet', '--quiet'),
            export_image_cmd_noimagefiles=migration_data.get('export_image_cmd_noimagefiles', '--noImageFiles'),
            export_image_cmd_poweroffsource=migration_data.get('export_image_cmd_poweroffsource', '--powerOffSource'),
            export_image_cmd_nonvramfile=migration_data.get('export_image_cmd_nonvramfile', '--noNvramFile'),
            export_image_cmd_acceptalleulas=migration_data.get('export_image_cmd_acceptalleulas', '--acceptAllEulas'),
            
            upload_image_ld_nfs_so_path=migration_data.get('upload_image_ld_nfs_so_path', '/x-v2v/iaas/lib/ld_nfs.so'),
            upload_image_dst_base_dir=migration_data.get('upload_image_dst_base_dir', 'v2v_upload'),
            upload_image_timeout=migration_data.get('upload_image_timeout', 86400),
            
            deal_image_src_format_vmdk=migration_data.get('deal_image_src_format_vmdk', 'vmdk'),
            deal_image_dst_format_qcow2=migration_data.get('deal_image_dst_format_qcow2', 'qcow2'),
            deal_image_convert_image_timeout=migration_data.get('deal_image_convert_image_timeout', 86400),
            deal_image_mount_base_dir=migration_data.get('deal_image_mount_base_dir', 'v2v_mount'),
            deal_image_file_lock_base_dir=migration_data.get('deal_image_file_lock_base_dir', 'v2v_lock'),
            
            create_instance_image_file_path=migration_data.get('create_instance_image_file_path', 'template.lz4'),
            create_instance_run_instance_timeout=migration_data.get('create_instance_run_instance_timeout', 1800),
            create_instance_start_instance_timeout=migration_data.get('create_instance_start_instance_timeout', 1200),
            create_instance_restart_instance_timeout=migration_data.get('create_instance_restart_instance_timeout', 1200),
            create_instance_stop_instance_timeout=migration_data.get('create_instance_stop_instance_timeout', 1200),
            create_instance_create_volumes_timeout=migration_data.get('create_instance_create_volumes_timeout', 1200),
            create_instance_attach_volumes_timeout=migration_data.get('create_instance_attach_volumes_timeout', 600),
            
            cover_image_timeout=migration_data.get('cover_image_timeout', 86400)
        )
        
        hyper_data = self._config_data.get('hyper', {})
        self._hyper = HyperConfig(
            image_base_dir=hyper_data.get('image_base_dir', '/data/images'),
            vmware_ovf_tool_path=hyper_data.get('vmware_ovf_tool_path', '/usr/bin/ovftool'),
            qemu_img_tool_path=hyper_data.get('qemu_img_tool_path', '/usr/bin/qemu-img'),
            container_mode=hyper_data.get('container_mode', 'local')
        )
        
        seed_data = self._config_data.get('seed', {})
        self._seed = SeedConfig(
            nodes=seed_data.get('nodes', ['192.168.1.100']),
            image_repository_base_dir=seed_data.get('image_repository_base_dir', '/data/repository'),
            id_rsa_path=seed_data.get('id_rsa_path', '/root/.ssh/id_rsa'),
            default_user=seed_data.get('default_user', 'root')
        )
        
        redis_data = self._config_data.get('redis', {})
        self._redis = RedisConfig(
            host=redis_data.get('host', '127.0.0.1'),
            port=redis_data.get('port', 6379),
            password=redis_data.get('password', ''),
            db=redis_data.get('db', 0),
            max_connections=redis_data.get('max_connections', 10),
            conf_name_v2v=redis_data.get('conf_name_v2v', 'x-v2v'),
            socket_timeout=redis_data.get('socket_timeout', 5),
            socket_connect_timeout=redis_data.get('socket_connect_timeout', 5),
            max_connection_number=redis_data.get('max_connection_number', 1000),
            key_prefix=redis_data.get('key_prefix', 'v2v_'),
            key_suffix_auto_node=redis_data.get('key_suffix_auto_node', 'auto')
        )
        
        zk_data = self._config_data.get('zk', {})
        self._zk = ZKConfig(
            hosts=zk_data.get('hosts', ['127.0.0.1:2181']),
            timeout=zk_data.get('timeout', 30000),
            x_v2v_zk_base_dir=zk_data.get('x_v2v_zk_base_dir', '/x-v2v'),
            dlock_key=zk_data.get('dlock_key', 'x-v2v'),
            dlock_timeout=zk_data.get('dlock_timeout', 5)
        )
        
        nfs_data = self._config_data.get('nfs', {})
        self._nfs = NFSConfig(
            mount_point=nfs_data.get('mount_point', '/mnt/nfs'),
            server=nfs_data.get('server', '192.168.1.200'),
            export_path=nfs_data.get('export_path', '/export/x-v2v')
        )
        
        log_data = self._config_data.get('log', {})
        self._log = LogConfig(
            level=log_data.get('level', 'INFO'),
            log_dir=log_data.get('log_dir', '/var/log/x-v2v'),
            max_bytes=log_data.get('max_bytes', 10485760),
            backup_count=log_data.get('backup_count', 5)
        )
        
        vmware_vsphere_data = self._config_data.get('vmware_vsphere', {})
        self._vmware_vsphere = VmwareVsphereConfig(
            timeout_connect_to_vmware_vsphere=vmware_vsphere_data.get(
                'timeout_connect_to_vmware_vsphere', 200
            )
        )
        
        self_data = self._config_data.get('self', {})
        self._self = SelfConfig(
            data_dir=self_data.get('data_dir', '/x-v2v/iaas/data'),
            deploy_dir=self_data.get('deploy_dir', '/x-v2v/iaas/deploy')
        )
        
        setting_data = self._config_data.get('setting', {})
        self._setting = SettingConfig(
            concurrency_migrate=setting_data.get('concurrency_migrate', 3),
            max_migrating_num=setting_data.get('max_migrating_num', 10),
            clean_after_failed=setting_data.get('clean_after_failed', True),
            vm_max_migrate_timeout=setting_data.get('vm_max_migrate_timeout', 86400)
        )
        
        resource_data = self._config_data.get('resource', {})
        self._resource = ResourceConfig(
            ld_nfs_so=resource_data.get('lib', {}).get('ld_nfs_so', '/x-v2v/iaas/lib/ld_nfs.so')
        )

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self._config_data
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    @property
    def project(self) -> ProjectConfig:
        return self._project

    @property
    def migration(self) -> MigrationConfig:
        return self._migration

    @property
    def hyper(self) -> HyperConfig:
        return self._hyper

    @property
    def seed(self) -> SeedConfig:
        return self._seed

    @property
    def redis(self) -> RedisConfig:
        return self._redis

    @property
    def zk(self) -> ZKConfig:
        return self._zk

    @property
    def nfs(self) -> NFSConfig:
        return self._nfs

    @property
    def log(self) -> LogConfig:
        return self._log

    @property
    def self(self) -> SelfConfig:
        return self._self

    @property
    def setting(self) -> SettingConfig:
        return self._setting

    @property
    def resource(self) -> ResourceConfig:
        return self._resource

    @property
    def vmware_vsphere(self) -> VmwareVsphereConfig:
        return self._vmware_vsphere

    @property
    def export_image_default_params(self) -> str:
        mig = self._migration
        log_level_cmd = "--X:logLevel=" + mig.export_image_log_level
        log_path_cmd = "--X:logFile=" + mig.export_image_log_path
        log_to_console_cmd = "--X:logToConsole" + mig.export_image_log_to_console
        return " ".join([
            mig.export_image_cmd_nosslverify,
            mig.export_image_cmd_overwrite,
            mig.export_image_cmd_machineoutput,
            mig.export_image_cmd_quiet,
            mig.export_image_cmd_noimagefiles,
            mig.export_image_cmd_poweroffsource,
            mig.export_image_cmd_nonvramfile,
            mig.export_image_cmd_acceptalleulas,
            log_level_cmd,
            log_path_cmd,
            log_to_console_cmd
        ])

    @property
    def export_image_cmd_log_level(self) -> str:
        return "--X:logLevel=" + self._migration.export_image_log_level

    @property
    def export_image_cmd_log_path(self) -> str:
        return "--X:logFile=" + self._migration.export_image_log_path

    @property
    def export_image_cmd_log_to_console(self) -> str:
        return "--X:logToConsole" + self._migration.export_image_log_to_console

    @property
    def export_image_dst_base_dir_full(self) -> str:
        return os.path.join(self._self.data_dir, self._migration.export_image_dst_base_dir)

    @property
    def upload_image_dst_base_dir_full(self) -> str:
        return os.path.join(self._self.data_dir, self._migration.upload_image_dst_base_dir)

    @property
    def deal_image_mount_base_dir_full(self) -> str:
        return os.path.join(self._self.data_dir, self._migration.deal_image_mount_base_dir)

    @property
    def deal_image_file_lock_base_dir_full(self) -> str:
        return os.path.join(self._self.data_dir, self._migration.deal_image_file_lock_base_dir)

    @property
    def create_instance_image_file_path_full(self) -> str:
        return os.path.join(self._self.deploy_dir, "statics", self._migration.create_instance_image_file_path)

    def reload(self) -> None:
        self._load_config(self._config_path)


config = Config()
