import logging
import os
from lura import fs
from lura.run import RunResult, run
from typing import List, Mapping, Sequence, Optional, Union

log = logging.getLogger(__name__)

#####
## helpers

class settings:

  git_bin: str = 'git'
  log_level: int = logging.DEBUG

Option = Union[str, int, float, bool, None]

def convert_opts(opts: Mapping[str, Option]) -> Sequence[str]:

  def convert_opt(name: str, value: Option) -> Optional[str]:
    name = name.replace('_', '-')
    if isinstance(value, (str, int, float)):
      value = str(value)
    elif isinstance(value, bool):
      if not value:
        return None
      value = None
    elif value is None:
      return None
    else:
      raise ValueError(f'Invalid value for git argument {name}: {value} ({type(value)})')
    return f'--{name}' if value is None else f'--{name}={value}'

  return tuple(
    opt
    for opt in (convert_opt(name, val) for name, val in opts.items())
    if opt is not None
  )

#####
## git functions

def git(
  cmd: str,
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  env: Optional[Mapping[str, str]] = None,
  cwd: Optional[str] = None,
) -> RunResult:
  argv = [settings.git_bin, cmd]
  argv.extend(args)
  argv.extend(convert_opts(opts))
  with run.log(log, settings.log_level):
    return run(argv, env=env, cwd=cwd)

def clone(
  *args: str,
  env: Optional[Mapping[str, str]] = None,
  cwd: Optional[str] = None,
  **opts: Option
) -> None:
  git('clone', args, opts, env, cwd)

def pull(
  *args: str,
  env: Optional[Mapping[str, str]] = None,
  cwd: Optional[str] = None,
  **opts: Option
) -> None:
  git('pull', args, opts, env, cwd)

def checkout(
  *args: str,
  env: Optional[Mapping[str, str]] = None,
  cwd: Optional[str] = None,
  **opts: Option
) -> None:
  git('checkout', args, opts, env, cwd)

def push(
  *args: str,
  env: Optional[Mapping[str, str]] = None,
  cwd: Optional[str] = None,
  **opts: Option
) -> None:
  git('push', args, opts, env, cwd)

#####
## repo wrapper

class Repo:

  _path: str
  _env: Optional[Mapping[str, str]]

  def __init__(
    self,
    path: str,
    env: Optional[Mapping[str, str]] = None
  ) -> None:

    super().__init__()
    self._path = path
    self._env = env

  @property
  def path(self) -> str:
    return self._path

  def clone(self, remote: str, **opts: Option) -> None:
    clone(remote, self._path, **opts, env=self._env)

  def pull(self, *args: str, **opts: Option) -> None:
    pull(*args, **opts, env=self._env, cwd=self._path)

  def checkout(self, *args: str, **opts: Option) -> None:
    checkout(*args, **opts, env=self._env, cwd=self._path)

  def push(self, *args: str, **opts: Option) -> None:
    push(*args, **opts, env=self._env, cwd=self._path)
