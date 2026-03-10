# -*- coding: utf-8 -*-
# @author: xiaobai

from pathlib import Path


def create_dir(file_name: str) -> Path:
    """ 创建文件夹 """
    path = Path(file_name).absolute().parent / file_name  # 拼接日志文件夹的路径
    if not Path(path).exists():  # 文件是否存在
        Path.mkdir(path)

    return path


