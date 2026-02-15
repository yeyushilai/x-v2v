#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Union
import libnfs


class NFSInterface:

    def __init__(self, address: str) -> None:
        if not address.startswith('nfs://'):
            address = 'nfs://' + address
        self.nfs: libnfs.NFS = libnfs.NFS(address)

    def readfile(self, path: str, mode: str = 'r') -> Union[str, bytes]:
        nfs_file = self.nfs.open(path, mode)
        data: Union[str, bytes] = nfs_file.read()
        nfs_file.close()
        return data

    def writefile(self, path: str, data: Union[str, bytes], mode: str = 'w') -> int:
        nfs_file = self.nfs.open(path, mode)
        bytes_written: int = nfs_file.write(data)
        return bytes_written

    def listdirs(self, path: str) -> list[str]:
        dirs: list[str] = self.nfs.listdir(path)
        tmp_dirs: list[str] = list()
        for d in dirs:
            if not (d == '.' or d == '..'):
                tmp_dirs.append(d)
        return tmp_dirs
