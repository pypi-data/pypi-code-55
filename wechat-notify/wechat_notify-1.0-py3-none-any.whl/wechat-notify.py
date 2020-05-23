import sys
import os
import subprocess
import requests
import time

def build_parser():
    if len(sys.argv) == 1:
        raise ValueError('please input command')
    return sys.argv[1:]

if __name__ == "__main__":
    try:
        token = os.environ['SERVER_CHAN_TOKEN']
    except KeyError:
        print('environment variable `SERVER_CHAN_TOKEN` unfound')
        exit(1)
    start = time.time()
    try:
        command = build_parser()
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, err = process.communicate()

    except KeyboardInterrupt:
        print('keyboard')
        process.kill()
        requests.post(r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Failed] command: ' + ' '.join(command) + f'&desp=start at {start}\ntake time: {duration}\nbecause of KeyboardInterrupt')

    duration = time.time() - start
    is_win = (sys.platform == 'win32')
    # import ipdb; ipdb.set_trace()
    if output is not None:
        output = output.decode('utf-8').split('\r\n') if is_win else output.decode('utf-8').split('\n')
    if err is not None:
        err = err.decode('utf-8').split('\r\n') if is_win else err.decode('utf-8').split('\n')
    if process.poll() == 0:
        temp = 'the following are last three lines of stdout:\n' + '\n'.join(output[-3:]) if output is not None else None
        post_str = r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Scuucess] command: ' + ' '.join(command) + f'&desp=start at {start}\ttake time: {duration}\t' + (temp if temp is not None else '')
        requests.post(post_str)
    else:
        temp = 'the following are last three lines of stderr:\n' + '\n'.join(err[-3:]) if err is not None else None
        # import ipdb; ipdb.set_trace()
        post_str = r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Failed] command: ' + ' '.join(command) + f'&desp=start at {start}\ttake time: {duration}\terror code: {process.poll()}'+ (temp if temp is not None else '')
        print(post_str)
        requests.post(post_str)
