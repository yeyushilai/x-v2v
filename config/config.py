# -*- coding: utf-8 -*-

"""
功能：配置管理类
"""

import os
import json
import yaml
from logger import logger
from config.default_config import DEFAULT_CONFIG


class Config:
    """
    配置管理类
    """

    def __init__(self, config_file=None, default_config=None):
        """
        初始化配置
        :param config_file: 配置文件路径
        :param default_config: 默认配置
        """
        self.config_file = config_file
        self.default_config = default_config or DEFAULT_CONFIG
        self._config = self._load_config()

    def _load_config(self):
        """
        加载配置
        """
        config = self.default_config.copy()

        # 如果指定了配置文件，加载配置文件
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    if self.config_file.endswith('.json'):
                        file_config = json.load(f)
                    elif self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                        file_config = yaml.safe_load(f)
                    else:
                        logger.warning("Unsupported config file format: {}".format(self.config_file))
                        return config

                # 合并配置
                self._merge_config(config, file_config)
                logger.info("Config loaded from file: {}".format(self.config_file))
            except Exception as e:
                logger.error("Failed to load config file: {}".format(e))

        return config

    def _merge_config(self, target, source):
        """
        合并配置
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_config(target[key], value)
            else:
                target[key] = value

    def get(self, key, default=None):
        """
        获取配置值
        :param key: 配置键，支持点号分隔的路径，如 "database.host"
        :param default: 默认值
        :return: 配置值
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        except Exception:
            return default

    def set(self, key, value):
        """
        设置配置值
        :param key: 配置键，支持点号分隔的路径，如 "database.host"
        :param value: 配置值
        """
        keys = key.split('.')
        config = self._config

        for i, k in enumerate(keys[:-1]):
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self, file_path=None):
        """
        保存配置到文件
        :param file_path: 保存路径，默认使用初始化时的配置文件路径
        """
        save_path = file_path or self.config_file
        if not save_path:
            logger.warning("No config file path specified, cannot save config")
            return False

        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                if save_path.endswith('.json'):
                    json.dump(self._config, f, indent=2, ensure_ascii=False)
                elif save_path.endswith('.yaml') or save_path.endswith('.yml'):
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                else:
                    logger.warning("Unsupported config file format: {}".format(save_path))
                    return False

            logger.info("Config saved to file: {}".format(save_path))
            return True
        except Exception as e:
            logger.error("Failed to save config file: {}".format(e))
            return False

    @property
    def config(self):
        """
        获取完整配置
        """
        return self._config
