import os
import json
import getpass
import shlex
import click
import paramiko

DEFAULT_PRIVATE_KEY = os.path.abspath(os.path.expanduser("~/.ssh/id_rsa"))
CMD_GET_HOSTNAME = """hostname"""
CMD_GET_PLATFORM = """/usr/bin/uname -a"""
CMD_GET_MAC = """/usr/sbin/ip addr | /bin/grep 'link/ether'| /bin/awk '{print $2}'"""
CMD_GET_CPU = """/bin/grep processor /proc/cpuinfo | /bin/wc -l"""
CMD_GET_MEMORY = """/bin/grep '^MemTotal:' /proc/meminfo | /bin/awk '{print $2}'"""
CMD_GET_DISK = """/bin/df -h | /bin/grep -i '/$' | awk '{print $2}'"""

UNIT_SIZES = {
    "k": 1024,
    "m": 1024*1024,
    "g": 1024*1024*1024,
    "t": 1024*1024*1024*1024,
    "p": 1024*1024*1024*1024*1024,
    "e": 1024*1024*1024*1024*1024*1024,
    "z": 1024*1024*1024*1024*1024*1024*1024,
    "y": 1024*1024*1024*1024*1024*1024*1024*1024,
}

def disk_byte_size(size):
    size = size.lower()
    if size.endswith("b"):
        size = size[:-1]
    unit = size[-1]
    number = int(size[:-1])
    return number * UNIT_SIZES[unit]

def get_ssh_result(ssh, cmd, type=None):
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode().strip()
        if type:
            result = type(result)
        return result
    except:
        return None

def ssh_get_sysinfo(host="localhost", port=22, user="root", private_key=DEFAULT_PRIVATE_KEY, password=None, **kwargs):
    hostname = None
    platform = None
    mac = None
    cpu = None
    memory = None
    disk = None
    cmd_get_hostname = kwargs.get("cmd_get_hostname", CMD_GET_HOSTNAME)
    cmd_get_platform = kwargs.get("cmd_get_platform", CMD_GET_PLATFORM)
    cmd_get_mac = kwargs.get("cmd_get_mac", CMD_GET_MAC)
    cmd_get_cpu = kwargs.get("cmd_get_cpu", CMD_GET_CPU)
    cmd_get_memory = kwargs.get("cmd_get_memory", CMD_GET_MEMORY)
    cmd_get_disk = kwargs.get("cmd_get_disk", CMD_GET_DISK)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        ssh.connect(host, port, user, password)
    else:
        rsa_key = paramiko.RSAKey.from_private_key_file(private_key)
        ssh.connect(host, port, user, pkey=rsa_key)

    hostname = get_ssh_result(ssh, cmd_get_hostname)
    platform = get_ssh_result(ssh, cmd_get_platform)
    mac = get_ssh_result(ssh, cmd_get_mac)
    cpu = get_ssh_result(ssh, cmd_get_cpu, type=int)
    memory = get_ssh_result(ssh, cmd_get_memory, type=int) * 1024
    disk = disk_byte_size(get_ssh_result(ssh, cmd_get_disk))

    data = {
        "hostname": hostname,
        "platform": platform,
        "mac": mac,
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
    }
    return data

@click.command()
@click.option("-h", "--host", default="localhost", help="default to localhsot.")
@click.option("-P", "--port", type=int, default=22, help="default to 22.")
@click.option("-u", "--user", default="root", help="default to root.")
@click.option("-i", "--private-key", default=DEFAULT_PRIVATE_KEY, help="default to ~/.ssh/id_rsa")
@click.option("-p", "--password", help="NO password means using public key auth.")
def main(host, port, user, private_key, password):
    try:
        sysinfo = ssh_get_sysinfo(host, port, user, private_key, password)
        print(json.dumps(sysinfo))
    except Exception as error:
        print(error)
        os.sys.exit(1)


if __name__ == "__main__":
    main()
