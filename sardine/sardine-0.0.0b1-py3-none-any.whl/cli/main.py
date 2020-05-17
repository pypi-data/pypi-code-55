import argparse

from sardine.actions.execute_stack import ExecuteStack
from sardine.actions.stop_stack import StopStack

commands = {
    'run': ExecuteStack,
    'stop': StopStack
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=('run', 'stop'), help="Command to run.")
    parser.add_argument("stack", help="Target stack alias.")
    parser.add_argument("-d", "--deattached", action='store_true', default=False,
                        help="Run the command in deattached mode.")
    args = parser.parse_args()

    command = commands[args.command]
    command.execute(args.stack, deattached=args.deattached)


if __name__ == '__main__':
    main()
