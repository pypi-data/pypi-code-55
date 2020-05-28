#!/usr/bin/env python3


import datetime
import platform
import argparse
import pprint
import sys
import socket
import subprocess
import shutil
import yaml
import jsons
import cpuinfo
import psutil
import uptime


def run(cmd):
    """execute a command and return its output"""
    return subprocess.getoutput(cmd)


def port_name(port):
    """convert port description in ufw to service name"""

    # some machines have a special format
    if '/' in port:
        port = port.split('/')[0]

    # table to translate port numbers to services
    table = {
        '22': 'ssh2',
        '2222': 'ssh2',
        '9001': 'tor',
        '9030': 'tor',
        '5432': 'psql',
        '3000': 'ide',
    }
    if port in table:
        return table[port]
    try:
        return socket.getservbyport(int(port))
    except:
        return port


def open_ports():
    """returns a list of the open ports"""

    # TODO: Do something not tied to the ufw utility in Ubuntu (which moreover only works as root)
    try:
        if shutil.which('ufw'):
            data = run('ufw status | grep ALLOW | grep -v v6')
            return sorted(set([port_name(line.split()[0])for line in data.splitlines()]))
    except:
        pass
    return None


def running_containers():
    """returns the number of docker containers running"""

    try:
        if shutil.which('docker'):
            data = run('docker container ls')
            return data.count('\n')
    except:
        pass
    return None


def information():
    """returns the monitoring information"""

    return {
        'time':
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'hostname':
            platform.node(),
        'system':
            platform.uname().system,
        'release':
            platform.uname().release,
        'uptime':
            uptime.uptime(),
        'load_avg':
            psutil.getloadavg(),
        'cpu_info':
            cpuinfo.get_cpu_info(),
        'logical_cpus':
            psutil.cpu_count(),
        'physical_cpus':
            psutil.cpu_count(logical=False),
        'cpus_freq':
            psutil.cpu_freq(percpu=True),
        'virtual_memory':
            psutil.virtual_memory(),
        'disk_partitions':
            psutil.disk_partitions(),
        'disk_usage':
            {
                p.mountpoint: psutil.disk_usage(p.mountpoint)
                for p in psutil.disk_partitions()
            },
        'sensors_temperatures':
            psutil.sensors_temperatures() if not psutil.MACOS else None,
        'sensors_fans':
            psutil.sensors_fans() if not psutil.MACOS else None,
        'sensors_battery':
            psutil.sensors_battery(),
        'ipmitool':
            # todo: call 'ipmitool delloem powermonitor' if possible and then parse it
            None,
        'running_containers':
            running_containers(),
        'running_processes':
            len(psutil.pids()),
    }


def main():
    """main function"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Monitor for worker machines in Jutge.org'
    )
    parser.add_argument(
        '--format',
        type=str,
        help='how to format the output (json|yaml|pprint|print)',
        default='json')
    parser.add_argument(
        '--indent',
        type=int,
        help='indentation for json and yaml',
        default=4)
    args = parser.parse_args()

    info = information()

    if args.format == 'json':
        print(jsons.dumps(info, indent=args.indent))
    elif args.format == 'yaml':
        print(yaml.dump(info, indent=args.indent, default_flow_style=False))
    elif args.format == 'pprint':
        pprint.pprint(info)
    elif args.format == 'print':
        print(info)
    else:
        print('unknown format (%s)' % args.format, file=sys.stderr)


if __name__ == '__main__':
    main()
