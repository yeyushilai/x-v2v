#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import tempfile
import subprocess
from typing import ClassVar, Optional, Tuple, Union


class CMDClient:

    @classmethod
    def normal_exec(cls, argv: Union[str, list[str]], timeout: int = 60) -> tuple[int, bytes, bytes]:
        """ 普通执行 """
        start_time = datetime.datetime.now()
        pipe = subprocess.Popen(argv,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)

        # pipe.poll()为None, 说明没有执行完毕
        while pipe.poll() is None:
            end_time = datetime.datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            if total_seconds > timeout:
                pipe.terminate()
                raise Exception(
                    "exec cmd timeout, cmd: %s, timeout: %s" % (argv, timeout))
            time.sleep(0.1)

        stdout, stderr = pipe.communicate()
        return pipe.returncode, stdout.strip(), stderr.strip()

    @classmethod
    def bash_exec(cls, cmd: str, timeout: int = 60, dir: str = '/tmp', bin: str = '/bin/bash -x ') -> tuple[int, bytes, bytes]:
        """ 使用bash命令执行 """
        tmp_file_path = tempfile.mktemp(suffix='.sh', prefix='_v2v_', dir=dir)
        with open(tmp_file_path, 'w') as f:
            f.write(cmd)
        cmd = f"{bin} {tmp_file_path} "

        # eg: /bin/bash -x /tmp/v2v_bash/_v2v_xMn1i_.sh
        return cls.normal_exec(cmd, timeout)
