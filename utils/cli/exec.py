# -*- coding: utf-8 -*-

"""
命令行工具
"""

import time
import datetime
import tempfile
import subprocess


def normal_exec(argv, timeout=60):
    start_time = datetime.datetime.now()
    pipe = subprocess.Popen(argv,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)

    # pipe.poll()为None 说明没有执行完毕
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


def bash_exec(cmd, timeout=60, dir=None, bin='/bin/bash -x '):
    if dir is None:
        dir = tempfile.gettempdir()
    tmp_file_path = tempfile.mktemp(suffix='.sh', prefix='_v2v_', dir=dir)
    with open(tmp_file_path, 'w') as f:
        f.write(cmd)
    cmd = "{bin} {tmp_file_path} ".format(bin=bin, tmp_file_path=tmp_file_path)
    # eg: /bin/bash -x /tmp/v2v_bash/_v2v_xMn1i_.sh
    return normal_exec(cmd, timeout)
