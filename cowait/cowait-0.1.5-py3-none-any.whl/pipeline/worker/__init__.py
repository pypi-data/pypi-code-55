import importlib

def execute(task_name):
    print('executing task:', task_name)

    module = importlib.import_module(task_name)
    print('module', module)

    task_class = getattr(module, 'Task')
    print('task', task_class)

    task = task_class()

    task.run()
