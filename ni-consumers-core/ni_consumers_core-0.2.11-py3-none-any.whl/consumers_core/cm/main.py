import importlib
import inspect
import os
import sys

from logging_utils import LogDecorator

from consumers_core import Action


@LogDecorator('is-package-inspect')
def _is_package(path):
    return (
        os.path.isdir(path)
        and os.path.exists(os.path.join(path, '__init__.py'))
    )


@LogDecorator("find-consumer-file-inspect")
def find_consumer_file(consumer_file):
    names=[consumer_file]

    if not names[0].endswith('.py'):
        names.append(names[0] + '.py')

    if os.path.dirname(names[0]):
        for name in names:
            expanded = os.path.expanduser(name)
            if os.path.exists(expanded):
                if name.endswith('.py') or _is_package(expanded):
                    return os.path.abspath(expanded)
    else:
        path = os.path.abspath('.')
        while True:
            for name in names:
                joined = os.path.join(path, name)
                if os.path.exists(joined):
                    if name.endswith('.py') or _is_package(joined):
                        return os.path.abspath(joined)
            parent_path = os.path.dirname(path)
            if parent_path == path:
                break
            path = parent_path


@LogDecorator(decorator_log='is-action-class-inspect', resume=True)
def is_action_class(item):
    return bool(
        inspect.isclass(item)
        and issubclass(item, Action)
        and not isinstance(item, Action)
    )


@LogDecorator(decorator_log='load-consumer_file-inspect')
def load_consumer_file(path):

    @LogDecorator(decorator_log='import-consumer_file-inspect')
    def __import_consumer_file__(filename):
        spec = importlib.util.spec_from_file_location(os.path.splitext(filename)[0], path)
        action = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(action)
        return action

    sys.path.insert(0, os.getcwd())
    directory, consumer_file = os.path.split(path)

    print(f'directory: {directory}, filename: {consumer_file}')
    added_to_path = False
    index = None

    if directory not in sys.path:
        print(f"not in sys.path: {sys.path}")
        sys.path.insert(0, directory)
        added_to_path = True
    else:
        i = sys.path.index(directory)
        print(f"in sys.path {sys.path} index value: {i}")
        if i != 0:
            index = i
            sys.path.insert(0, directory)
            del sys.path[i + 1]

    imported = __import_consumer_file__(consumer_file)

    if added_to_path:
        del sys.path[0]

    if index is not None:
        sys.path.insert(index + 1, directory)
        del sys.path[0]

    consumer_classes = {name:value for name, value in vars(imported).items() if is_action_class(value)}
    return imported.__doc__, consumer_classes
