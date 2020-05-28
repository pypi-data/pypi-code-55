#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : app.py
@Author: donggangcj
@Date  : 2019-07-09
@Desc  : 从指定路径目录复制指定类型到指定目录
            1. 判断输入源地址和目的地址是否存在
            2. 文件类型只能是markdown和图片类型
            3. 是否需要更新已存在图片
            4. 执行完，push到代码仓
            5. 代码仓自动出发travis脚本，release(Jsdelivr)(通过开源工具release-it)
            6.
'''
import imghdr
import os
import shutil
import subprocess

import click


@click.command()
@click.option("--source_dir", default='/Users/donggang/Documents/blog-new/source', help="源目录地址")
@click.option("--target_dir", default='/Users/donggang/Documents/cdn-github-jsdeliver/CDN/image', help="目的目录地址")
@click.option("--file_type", default='image', help="文件类型,支持markdown,image两种类型")
@click.option('--verbose', '-v', is_flag=True, help='显示详细信息')
@click.option('--release', is_flag=True, help="发布")
@click.option('--git_repo', default='/Users/donggang/Documents/cdn-github-jsdeliver/CDN', help='代码仓地址')
# @click.option("--")
# @click.option("--override/--no-override", default=True, help="是否覆盖已存在文件,默认覆盖")
def sync(source_dir, target_dir, file_type, verbose, release, git_repo):
    """Copy anything from anywhere to anywhere"""
    click.secho("==> SYNC TO LOCAL REPO", fg='magenta')
    file_account = 0
    if not os.path.exists(source_dir):
        click.secho("Source_dir %s not existed" % source_dir, err=True, fg='yellow')
        exit(0)
    if not os.path.exists(target_dir):
        click.secho("Target_dir %s not existed" % target_dir, err=True, fg='yellow')
        exit(0)

    for dir, dirnames, filename in os.walk(source_dir):
        for file in filename:
            abs_path_of_file = os.path.join(dir, file)
            if imghdr.what(abs_path_of_file) is not None:
                # Target path include file name
                dts_path_of_file = os.path.join(target_dir, os.path.split(dir)[1], file)
                # Target directory
                dts_path = os.path.join(target_dir, os.path.split(dir)[1])
                if not os.path.exists(dts_path):
                    os.mkdir(dts_path)
                shutil.copy(abs_path_of_file, dts_path_of_file)
                file_account = file_account + 1
                if verbose:
                    click.secho("%s --> %s" % (abs_path_of_file, dts_path_of_file))
    click.secho("COPY SUCCESSFULLY[%s files have been copied]" % file_account, fg="cyan")
    if release:
        click.secho("==> RELEASE TO GITHUB", fg='magenta')
        r = release_it(git_repo)
        if r == 0:
            click.secho("==> OK")
        else:
            click.secho("==> FAIL")


# def check_file_type(file_type):
#     pass


def release_it(git_repo):
    command_string = 'cd {} && git add . && git commit -m "同步" && release-it --ci'.format(git_repo)
    release_result = subprocess.run(command_string, shell=True)
    return release_result


if __name__ == '__main__':
    sync()
