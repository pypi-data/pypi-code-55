from Utils.Subprocess import run
from time import sleep


# TODO resource monitor

def resource_monitor():
    last_idle = last_total = 0
    while True:
        with open('/proc/stat') as cpu:
            fields = [float(column) for column in cpu.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle, total - last_total
        last_idle, last_total = idle, total
        cpu_stat = 100.0 * (1.0 - idle_delta / total_delta)

        print('Overall CPU Usage: %5.1f%%' % cpu_stat, end='\r')
        sleep(1)


def memory():
    with open('/proc/meminfo', 'r') as mem:
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                total = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
        free = tmp
        mem_stat = int(total) - int(free)

    print(f"Memory usage: {mem_stat}")
