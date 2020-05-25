import os.path
from .task_image import TaskImage

def build(task: str):
    image = TaskImage.create(task)
    print('context path:', image.root)

    # find task-specific requirements.txt
    # if it exists, it will be copied to the container, and installed
    requirements = image.find_file_rel('requirements.txt')
    if requirements:
        print('found custom requirements.txt:', requirements)

    # find custom Dockerfile
    # if it exists, build it, then extend that instead of the default base image
    dockerfile = image.find_file('Dockerfile')
    if dockerfile:
        print('found custom Dockerfile:', os.path.relpath(dockerfile, image.root))
        print('building custom base image...')
        logs = image.build_custom_base(dockerfile)
        for log in logs:
            if 'stream' in log:
                print(log['stream'], flush=True, end='')
    
    print('building task image...')
    logs = image.build(
        requirements=requirements,
    )

    for log in logs:
        if 'stream' in log:
            print(log['stream'], flush=True, end='')

    return image


def run(task: str):
    image = build(task)

    # run container
    container = image.run()

    print('--- TASK OUTPUT: -------------------------------------')
    for log in container.logs(stream=True):
        print(str(log, encoding='utf-8').strip(), flush=True)
    print('------------------------------------------------------')

    # destroy container
    container.remove(force=True)


def push(task: str):
    image = build(task)

    print('pushing...')
    logs = image.push('814891515109.dkr.ecr.us-east-1.amazonaws.com/ds-pipeline-task-test')
    for log in logs:
        pass

    print('done')