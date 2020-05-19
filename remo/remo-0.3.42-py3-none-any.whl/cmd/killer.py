import psutil
import socket
from multiprocessing import Process
import requests


def is_remo_app(config):
    try:
        resp = requests.get('{}/version'.format(config.get_host_address())).json()
        return resp.get('app') == 'remo'
    except Exception:
        pass
    return False


def try_to_terminate_another_remo_app(config):
    if is_remo_app(config):
        confirm = input(
            'Another instance of remo-app is running on port {}, do you want to stop it and start a new one? [Y/N]: '.format(
                config.port))
        if confirm.lower() in ('y', 'yes'):
            terminate_remo(config)

            if is_port_in_use(config.port):
                print('Failed to terminate the remo-app, port {} still in use'.format(config.port))
            else:
                return True
    return False


def kill_ui_process(ui_process):
    if isinstance(ui_process, Process) and ui_process.is_alive():
        ui_process.terminate()

    print('\nRemo was stopped.')


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0

def terminate_remo(config):
    terminate_remo_app(config)
    terminate_electron_app()


def _find_processes(name="", starts_with=""):
    pids = []
    for proc in psutil.process_iter():
        try:
            info = proc.as_dict(attrs=['pid', 'name'])
            if info and info['name']:
                process_name = info['name'].lower()
                if name and name == process_name:
                    pids.append(info['pid'])
                elif starts_with and process_name.startswith(starts_with):
                    pids.append(info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return pids


def terminate_electron_app():
    pids = _find_processes(starts_with='remo')
    _kill_pids(pids)


def _kill_pids(pids):
    try:
        for pid in pids:
            p = psutil.Process(pid)
            _terminate_process(p)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass


def _terminate_process(p: psutil.Process):
    try:
        p.terminate()
        p.wait(2)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired):
        pass


def terminate_remo_app(config):
    port = int(config.port)
    pids = _find_processes(starts_with='python')
    try:
        for pid in pids:
            p = psutil.Process(pid)
            connections = p.connections("inet4")
            if len(connections):
                conn = connections[0]
                if config.is_local_server():
                    if conn.laddr and conn.laddr.port == port:
                        _terminate_process(p)
                else:
                    if conn.raddr and conn.raddr.port == port:
                        _terminate_process(p)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
