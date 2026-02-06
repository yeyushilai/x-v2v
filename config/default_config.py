# -*- coding: utf-8 -*-

"""
功能：默认配置
"""

import socket


# 当前节点信息
LOCAL_NODE_ID = socket.gethostname().strip()
LOCAL_NODE_IP = socket.gethostbyname(LOCAL_NODE_ID)


DEFAULT_CONFIG = {
    "common": {
        "max_migrating_num": 10,
        "data_dir": "/tmp/v2v",
        "concurrency_migrate": True,
        "indeed_start_migrate_timeout": 300,
        "indeed_end_migrate_timeout": 3600,
        "clean_after_failed": True
    },
    "export_image": {
        "dst_base_dir": "/tmp/v2v/export",
        "log_path": "/tmp/v2v/export.log",
        "timeout": 86400,
        "max_retry_times": 5,
        "cmd_vi_prefix": "vi://",
        "default_params": "--noSSLVerify --overwrite --machineOutput --quiet --noImageFiles --powerOffSource --noNvramFile --acceptAllEulas --X:logLevel=warning --X:logFile=/tmp/v2v/export.log",
        "dst_format_ova": "ova"
    },
    "upload_image": {
        "dst_base_dir": "/tmp/v2v/upload",
        "timeout": 86400
    },
    "server": {
        "conf": {}
    },
    "zk": {
        "base_dir": "/v2v/worker"
    },
    "pg": {
        "min_connect": 1,
        "max_connect": 100
    },
    "redis": {
        "conf_name_v2v": "v2v",
        "key_prefix": "v2v",
        "key_suffix_auto_node": "auto_node"
    },
    "template": {
        "ssh_cmd_option": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
        "ssh_cmd_template": "ssh {option} {user}@{host} \"{cmd}\"",
        "scp_cmd_template": "scp {option} {src_path} {user}@{host}:{dst_path}",
        "export_image_cmd_template": "export_image --src-vm-id {src_vm_id} --dst-format {dst_format} --dst-path {dst_path}",
        "deal_image_convert_image_cmd_template": "qemu-img convert -f qcow2 -O raw {src_image_path} {dst_image_path}",
        "create_instance_insert_image_template": "create_instance --name {vm_name} --type {vm_type} --cpu {cpu} --memory {memory} --image {image_id} --network {network}"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "v2v.log"
    }
}
