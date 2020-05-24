from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError, PIPE, run
from typing import List, Sequence, Set, Union

from multi_docker_build.build_docker_containers import build as build_images, read_images

# TODO: consider using a package like 'gitpython' for this. It's
#  straightforward enough to run Git like this

GIT = 'git'

class GitCommandRunner:
    def __init__(self, pretend: bool, push: bool):
        self.pretend = pretend
        self.should_push = push

    def __call__(self, *args: Sequence[str], **subprocess_kwargs):
        if args and args[0] == 'push':
            message = 'Use GitCommandRunner.push instead (due to special push override functionality)'
            raise ValueError(message)
        command = [GIT, *args]
        command_str = ' '.join(command)
        if self.pretend:
            print('Would run', command_str)
        else:
            print('Running', command_str)
            return run(command, check=True, **subprocess_kwargs)

    def push(self, *args: Sequence[str], **subprocess_kwargs):
        if self.should_push:
            self('push', *args, **subprocess_kwargs)
        else:
            print('Would push with args', args)

    def get_branches(self) -> Set[str]:
        with self.pretend_override():
            output_proc = self('branch', '-a', stdout=PIPE)
            lines: List[bytes] = output_proc.stdout.splitlines()
        return {line[2:].strip().decode() for line in lines}

    # TODO: rethink this
    @contextmanager
    def pretend_override(self):
        old_pretend = self.pretend
        self.pretend = False
        yield
        self.pretend = old_pretend

DO_NOT_SIGN = object()
SIGN_WITH_DEFAULT_IDENTITY = object()

def adjust_dockerfile_tags(tag_without_v: str, pretend: bool = False):
    docker_images = read_images(Path())
    labels = set(label for label, path, options in docker_images)

    for cwl_file in Path().glob('**/*.cwl'):
        # Not worth parsing this as YAML. We want minimal diffs
        # between the previous version and our modifications
        lines = cwl_file.read_text().splitlines()
        new_lines = []
        for line in lines:
            line = line.rstrip()
            if 'dockerPull' in line:
                pieces = line.split(':', 1)
                image = pieces[1].strip().split(':')[0].strip('"')
                if image in labels:
                    print('Found managed Docker image', image, 'in', cwl_file)
                    pieces[1] = f'{image}:{tag_without_v}'
                    line = ': '.join(pieces)
            new_lines.append(line)
        if not pretend:
            with open(cwl_file, 'w') as f:
                for line in new_lines:
                    print(line, file=f)

def tag_release_pipeline(tag: str, sign: Union[object, str], pretend: bool = False, push: bool = True):
    tag_without_v = tag.lstrip('v')

    git = GitCommandRunner(pretend, push)
    git('checkout', 'master')
    try:
        git('pull', '--ff-only')
    except CalledProcessError as e:
        message = 'Your `master` branch and `origin/master` have divergent history'
        raise ValueError(message) from e
    branches = git.get_branches()
    if 'remotes/origin/release' in branches:
        if 'release' in branches:
            git('checkout', 'release')
            git('pull', '--ff-only')
        else:
            git('checkout', '-b', 'release', 'origin/release')
    else:
        if 'release' in branches:
            git('checkout', 'release')
        else:
            git('checkout', '-b', 'release')
        git.push('-u', 'origin', 'release')
    git('merge', 'master')
    git('submodule', 'update', '--init', '--recursive')
    build_images(
        tag_timestamp=False,
        tag=tag_without_v,
        push=push,
        ignore_missing_submodules=False,
        pretend=pretend,
    )
    adjust_dockerfile_tags(tag_without_v, pretend)
    git('commit', '-a', '-m', f'Update container tags for {tag}')

    tag_extra_args = []
    if sign is DO_NOT_SIGN:
        tag_extra_args.append('-a')
    elif sign is SIGN_WITH_DEFAULT_IDENTITY:
        tag_extra_args.append('-s')
    else:
        tag_extra_args.extend(
            [
                '-s',
                '-u',
                sign,
            ],
        )
    git('tag', tag, *tag_extra_args)
    git.push()
    git.push('--tags')
    git('checkout', 'master')
    git.push()

def main():
    p = ArgumentParser()
    p.add_argument(
        'tag',
        help="""
            Tag name to use, both in the pipeline Git repository and for
            any Docker images built for this pipeline.
        """,
    )
    p.add_argument(
        '--sign',
        nargs='?',
        default=DO_NOT_SIGN,
        const=SIGN_WITH_DEFAULT_IDENTITY,
        help="""
            Sign the new tag. If given a value, e.g. '--sign=your@email.address',
            sign with the GPG key associated with that identity. If given as
            '--sign', sign the tag with your default GPG identity.
        """,
    )
    p.add_argument(
        '--pretend',
        action='store_true',
        help="""
            Run in pretend mode: don't actually execute anything (tagging or 
            pushing commits, building, tagging, or pushing container images).
        """,
    )
    p.add_argument(
        '--no-push',
        action='store_true',
        help="""
            Run everything locally (switching and merging branches, making a
            new Git tag, building Docker containers), but don't push anything
            to Docker Hub or the Git remote repository.
        """,
    )
    args = p.parse_args()

    tag_release_pipeline(
        tag=args.tag,
        sign=args.sign,
        pretend=args.pretend,
        push=not args.no_push,
    )

if __name__ == '__main__':
    main()
