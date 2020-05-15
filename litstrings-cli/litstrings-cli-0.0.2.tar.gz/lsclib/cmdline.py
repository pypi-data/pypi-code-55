#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click
import requests
import configparser

__author__ = "Iridium Intelligence"

lsUrl = "https://litstrings.info/"

@click.group()
def main():
    """
    Simple CLI for interacting with LitStrings
    """
    pass

@main.command()
@click.argument('pid')
def init(pid):
    """Initiate LS project by creating config file in pwd directory where command being used from. You need to provide project unique id to be able to use LitStrings cloud translation management services. If you plan to use LS as open source library without need of our cloud services, you can use any value as PID """
    pwd = os.getcwd()
    config = configparser.ConfigParser()
    if os.path.exists(".litstrings"):
        config.read('.litstrings')
        print('PID: '+config['project_data']['pid'])
        response = 'Project already initiated'
    else:
        config.add_section('project_data')
        config.set('project_data', 'pid', pid)
        config.set('project_data', 'path', pwd)
        with open('.litstrings', 'w') as configfile:    # save
            config.write(configfile)
        response = 'Project initiated'
    click.echo(response)


@main.command()
def status():
    """Get information about the project"""
    config = configparser.ConfigParser()
    if os.path.exists(".litstrings"):
        config.read('.litstrings')
        response = 'PID: '+config['project_data']['pid']
    else:
        response = 'Project not yet initiated'
    click.echo(response)


@main.command()
def languages_remote():
    """List all languages registered at LitStrings, connected to this project"""

    if os.path.exists(".litstrings"):
        config = configparser.ConfigParser()
        config.read('.litstrings')
        url_format = lsUrl+'api/v1/project/'+config['project_data']['pid']+'/languages'
        response = requests.get(url_format).json()
        for x in response:
            print x
    else:
        response = 'Project not yet initiated'


        click.echo(response)

if __name__ == "__main__":
    main()