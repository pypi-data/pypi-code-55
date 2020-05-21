#!/usr/bin/python3 
# -*- coding: utf-8 -*- 
#author zhouh zhouhui295@163.com 2014-7-22

import os
import click

from .s3 import command as s3cmd
from .jump import command as jumpCmd


@click.group()
def entry_point():
    pass

@click.command()
def help():
    click.echo('command line tools help')

entry_point.add_command(help)
entry_point.add_command(s3cmd.s3)
entry_point.add_command(jumpCmd.jump)
