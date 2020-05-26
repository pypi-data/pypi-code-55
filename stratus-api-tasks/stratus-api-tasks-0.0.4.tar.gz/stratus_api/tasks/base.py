def create_celery_app(project_folder):
    """Creates a celery app based on the celery setting pulled from environment variables.
        DO NOT DELETE the `import tasks`

        :return: celery app
        """
    from stratus_api.core.settings import get_settings
    from celery import Celery
    celery_settings = get_settings(settings_type='celery')
    celery_app = Celery(__name__)
    celery_settings['imports'] = collect_app_tasks(project_folder=project_folder) + ['handlers', 'routes']
    celery_app.config_from_object(celery_settings, force=True)
    import_tasks = collect_framework_tasks()
    for pkg, file in import_tasks:
        celery_app.autodiscover_tasks(packages=[pkg], related_name=file, force=True)
    return celery_app


def collect_app_tasks(project_folder):
    import os
    tasks = set()
    for i in os.walk(os.path.join(project_folder, 'tasks')):
        base = i[0].replace(project_folder, '').replace('/', '.').strip('.')
        tasks.add(base)
        for f in [f.replace('.py', '') for f in i[-1] if
                  f.endswith('.py') and f not in {'__init__.py'} and "pycache" not in f]:
            tasks.add(base + '.' + f)
    return list(tasks)


def collect_framework_tasks():
    import os
    framework_dir = os.path.abspath(__file__).replace('/tasks/base.py', '')
    tasks = list()
    for root, folders, files in os.walk(framework_dir):
        if ('tasks' in root and 'stratus_api/tasks' not in root) or 'stratus_api/tasks/tasks' in root:
            base = root.replace(framework_dir, 'stratus_api').replace('/', '.')
            for f in [f.replace('.py', '') for f in files if
                      f.endswith('.py') and f not in {'__init__.py'} and "pycache" not in f]:
                tasks.append((base, f))
    return tasks
