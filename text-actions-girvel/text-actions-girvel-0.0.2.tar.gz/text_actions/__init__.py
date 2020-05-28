def ui_action(actions, *commands):
    def decorator(func):
        actions.append((commands, func))
    return decorator


def apply_action(actions, input_string, state):
    """Throws TypeError, if number of arguments is incorrect, and ValueError, if types of arguments do not match.
    Returns True, if any command was executed, otherwise False"""
    args = input_string.split(' ')
    for commands, action in actions:
        if args[0] in commands:
            action(state, *args[1:])
            return True
    return False