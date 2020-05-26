from preapp.utils.database import Database

__hooks_db__ = Database()


def action_hook(*args):
    global __hooks_db__

    def inner(function):
        __hooks_db__.iterload(args, [function])

    return inner


def call_hook(*args):
    for func in __hooks_db__[args]:
        func()
