#!/usr/bin/python
# coding=utf-8
#pyyaml

import click
import os
import yaml
import uuid

import src.config

# Config
temp_dir = '/tmp'
roles_folder = './local_roles'

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name', default='')
def install(name):
    '''
    install dependency from meta/main.yml in local folder
    '''
    # check ansible-galaxy exist
    if os.system("ansible-galaxy --version > /dev/null ") != 0:
        click.echo(click.style('✘ Ansible-galaxy not found!\nPlease install ansible on youre host or, \nyou can manualy set path to ansible-galaxy bin,\nuse GALAXY_PATH env, or galaxy_path config options',
          fg='red'), err=True)
    click.echo(click.style(
        '✓ Ansible-galaxy bin found', fg='green'))

    # check meta/main.yml exist
    if not os.path.exists('meta/main.yml'):
        click.echo(click.style(
            '✘ file meta/main.yml not found', fg='red'), err=True)
        exit(1)
    # read data from meta/main.yml
    with open("meta/main.yml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            if data is None:
                click.echo(click.style(
                    '✘ File meta/main.yml is empty', fg='red'), err=True)
                exit(1)
            if not 'dependencies' in data:
                click.echo(click.style(
                    '✘ Dependencies list not found in meta/main.yml', fg='red'), err=True)
                exit(1)
            if 'dependencies' in data and len(data['dependencies']) == 0:
                click.echo(click.style(
                    '? Dependencies list is empty\n\nI have nothing to do ....', fg='yellow'))
                exit(0)
            click.echo(click.style(
                '✓ File meta/main.yml is valid', fg='green'))

            # Generate file reqs.yml
            uuid_var = str(uuid.uuid4())
            path = "%s/ansible-%s.yml" % (temp_dir, uuid_var)

            # validation
            # for i in data['dependencies']:
            #     click.echo(i)

            # generate data for write in yml
            reqs_data = {
                'roles': data['dependencies']
            }

            # write data in install yaml file
            with open(path, 'w') as yamlfile:
                yaml.dump(reqs_data, yamlfile, default_flow_style=False)
            click.echo(click.style(
                '✓ The file with dependencies is ready\nInstalling to %s folder ...' % roles_folder, fg='green'))

            # Install from file reqs.txt
            if os.path.exists(path):
                install_res = os.system('ansible-galaxy install -r %s -p %s --force' %
                          (path, roles_folder))
                if install_res == 0:
                    click.echo(click.style(
                        '✓ All dependencies were successfully installed\n\nHappy ansibling :)', fg='green'))
                    os.remove(path)
                    exit(0)
                if install_res != 0:
                    click.echo(click.style(
                        '✘ An error occurred while installing dependencies', fg='red'), err=True)
                    os.remove(path)
                    exit(1)

        except yaml.YAMLError as exc:
            click.echo(click.style(exc, fg='red'), err=True)


if __name__ == '__main__':
    cli()
