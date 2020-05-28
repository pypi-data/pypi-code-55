import os
import platform
from time import time, strftime, localtime, gmtime
import termcolor

from organizer.actions import actions
from text_actions import apply_action


def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def tts(t, relative=False):
    return strftime('%H:%M', (gmtime if relative else localtime)(t))


class State:
    def __init__(self):
        self.starting_time = time()
        self.activities = []  # activity is (name, starting time, ending time)


state = State()

if __name__ == '__main__':
    clear()
    print('Welcome to organizer, master')
    input()
    while True:
        clear()
        total_time = (state.activities[-1][2] - state.starting_time) if state.activities else 0
        print(
            termcolor.colored(
                'Started at {started}{tab1}Now is {current}{tab2}Spent {spent}\n'.format(
                    started=tts(state.starting_time),
                    current=tts(time()),
                    spent=tts(total_time, True),
                    tab1=' ' * 14,
                    tab2=' ' * 18,
                ),
                "grey",
                "on_white"
            )
        )
        print(*(f' {i + 1}\t{tts(a[1])}\t{tts(a[2])}\t{a[0]}' for i, a in enumerate(state.activities)), sep='\n')
        print()
        if state.activities:
            parts = dict()
            for a in state.activities:
                if a[0] not in parts:
                    parts[a[0]] = 0
                parts[a[0]] += a[2] - a[1]
            print(
                *(
                    '{percentage}%\t{time}\t{activity}'.format(
                        percentage=round(v / total_time * 100),
                        time=tts(v, True),
                        activity=k) for k, v in {**parts, "doing nothing": total_time - sum(parts.values())}.items()
                ),
                sep='\n',
                end='\n\n'
            )
        action = input(':')
        if not action:
            continue
        else:
            try:
                if not apply_action(actions, action, state):
                    state.activities.append([action, time(), time()])
            except TypeError:
                input(f'This action has different signature\n')
            except ValueError:
                input(f'This action has other types of arguments\n')
