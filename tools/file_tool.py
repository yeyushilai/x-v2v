#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import yaml
import hashlib
from typing import Optional, Any, Union


class FileTool:

    @classmethod
    def compare_file_size(cls, file_a: str, file_b: str) -> int:
        """比较文件大小"""
        assert file_a
        assert file_b

        file_a_size: int = os.path.getsize(file_a)
        file_b_size: int = os.path.getsize(file_a)

        if file_a_size > file_b_size:
            return 1
        if file_a_size == file_b_size:
            return 0
        else:
            return -1

    @classmethod
    def create_replica_file(cls, file_path: str) -> Optional[str]:
        """创建文件的副本"""
        if not os.path.exists(file_path):
            print("源文件路径不存在，请检查后重试")
            return None

        # 获取原始文件的父路径和文件名并解析文件名
        parent_path, file_name = os.path.split(file_path)
        file_name_prefix, file_name_suffix = os.path.splitext(file_name)

        # 生成副本文件名称和路径
        replica_file_name: str = file_name_prefix
        replica_file_name += ' - 副本'
        replica_file_name += file_name_suffix
        replica_file_path: str = os.path.join(parent_path, replica_file_name)

        # 判断目录下是否已经存在合法副本文件
        if os.path.exists(replica_file_path) and cls.compare_file_size(file_path, replica_file_path) == 0:
            print("同目录下已经存在副本文件，无需重复创建！")
            return None

        # 源文件读取数据，副本文件写入数据
        with open(file_path, encoding='utf8') as file:
            with open(replica_file_path, 'w', encoding='utf8') as f:
                for row_data in file.readlines():
                    f.write(row_data)

        print("创建文件副本成功")
        return replica_file_path

    @classmethod
    def get_file_size(cls, file_path: str, unit: Optional[str] = None) -> Union[int, float]:
        size_in_bytes: int = os.path.getsize(file_path)

        unit = unit or "b"
        if unit == "b":
            return size_in_bytes
        elif unit == "kb":
            return size_in_bytes / 1024
        elif unit == "mb":
            return size_in_bytes / 1024 / 1024
        elif unit == "gb":
            return size_in_bytes / 1024 / 1024 / 1024
        elif unit == "tb":
            return size_in_bytes / 1024 / 1024 / 1024 / 1024
        elif unit == "pb":
            return size_in_bytes / 1024 / 1024 / 1024 / 1024 / 1024
        elif unit == "eb":
            return size_in_bytes / 1024 / 1024 / 1024 / 1024 / 1024 / 1024
        elif unit == "zb":
            return size_in_bytes / 1024 / 1024 / 1024 / 1024 / 1024 / 1024 / 1024
        elif unit == "yb":
            return size_in_bytes / 1024 / 1024 / 1024 / 1024 / 1024 / 1024 / 1024 / 1024
        else:
            raise ValueError("Unit value error")

    @classmethod
    def search_file_in_dir(cls, file_name: str, directory: str) -> Optional[str]:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == file_name:
                    return os.path.join(root, file)
        return None

    @classmethod
    def read_json_file(cls, file_path: str) -> dict[str, Any]:
        if not file_path:
            return dict()

        with open(file_path, encoding="utf-8") as f:
            return json.loads(f.read())

    @classmethod
    def read_yaml_file(cls, file_path: str) -> Optional[Any]:
        if not file_path:
            return dict()

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(f"Error reading YAML file: {e}")
                return None

    @classmethod
    def calculate_md5(cls, file_path: str, buffer_size: int = 8192) -> str:
        md5_hash = hashlib.md5()

        with open(file_path, 'rb') as file:
            while chunk := file.read(buffer_size):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()

    @classmethod
    def calculate_sha1(cls, file_path: str, buffer_size: int = 8192) -> str:
        sha1_hash = hashlib.sha1()

        with open(file_path, 'rb') as file:
            while chunk := file.read(buffer_size):
                sha1_hash.update(chunk)

        return sha1_hash.hexdigest()

    @classmethod
    def calculate_sha256(cls, file_path: str, buffer_size: int = 8192) -> str:
        sha256_hash = hashlib.sha256()

        with open(file_path, 'rb') as file:
            while chunk := file.read(buffer_size):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()

    @classmethod
    def calculate_hash(cls, file_path: str, buffer_size: int = 8192) -> dict[str, str]:
        md5_hash = hashlib.md5()
        sha1_hash = hashlib.sha1()
        sha256_hash = hashlib.sha256()

        with open(file_path, 'rb') as file:
            while chunk := file.read(buffer_size):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)

        return dict(
            md5=md5_hash.hexdigest(),
            sha1=sha1_hash.hexdigest(),
            sha256=sha256_hash.hexdigest()
        )


if __name__ == '__main__':
    print(FileTool.calculate_hash("text_tool.py"))
    print(FileTool.get_file_size("text_tool.py", "mb"))
    print(FileTool.read_yaml_file("config.yaml"))
