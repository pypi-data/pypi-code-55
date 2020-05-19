import os


FILENAME = os.path.join(os.path.expanduser('~'), 'deep_space_trader_log.txt')


def log_message(msg):
    with open(FILENAME, 'a') as fh:
        fh.write(msg + '\n')
