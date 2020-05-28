from time import time
from text_actions import ui_action

actions = []


def action(*commands):
    return ui_action(actions, *commands)


@action('quit', 'exit')
def end_application(state):
    quit()


@action('e', 'end')
def end_last_action(state):
    state.activities[-1][2] = time()


@action('d', 'delete')
def delete_action(state, index='-1'):
    index = int(index)
    if index < 0:
        index += len(state.activities)
    state.activities = state.activities[:index] + state.activities[index + 1:]


@action('s', 'save')
def save_state(state, filename='current.org'):
    with open(filename, 'w') as f:
        f.write(str(state.starting_time))
        f.write('\n')
        f.write('\n'.join('\t'.join(str(e) for e in a) for a in state.activities))


@action('open')
def read_state(state, filename):
    with open(filename, 'r') as f:
        content = f.read().split('\n')

    state.starting_time = float(content[0])
    content = content[1:]

    if not content[-1]:
        content = content[:-1]

    content = [e.split('\t') for e in content]
    state.activities = [[e[0], float(e[1]), float(e[2])] for e in content]
