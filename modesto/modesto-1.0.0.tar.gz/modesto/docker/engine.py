import logging
import json
from lura.run import RunResult, run
from typing import cast, List, Mapping, Optional, Sequence, Union

log = logging.getLogger(__name__)

#####
## helpers

class settings:

  docker_bin: str = 'docker'
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
      raise ValueError(f'Invalid value for docker argument {name}: {value} ({type(value)})')
    return f'--{name}' if value is None else f'--{name}={value}'

  return tuple(
    opt
    for opt in (convert_opt(name, val) for (name, val) in opts.items())
    if opt is not None
  )

#####
## docker

def docker(
  cmd: str,
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  cwd: Optional[str] = None,
  enforce: Optional[bool] = True,
) -> RunResult:

  argv: List[str] = [settings.docker_bin, cmd]
  argv.extend(args)
  argv.extend(convert_opts(opts))
  with run.log(log, settings.log_level):
    return run(argv, cwd=cwd, enforce=enforce)

def build(cwd: Optional[str] = None, *args: str, **opts: Option) -> None:
  docker('build', args, opts, cwd=cwd)

def tag(*args: str, **opts: Option) -> None:
  docker('tag', args, opts)

def push(*args: str, **opts: Option) -> None:
  docker('push', args, opts)

def images(*args: str, **opts: Option) -> Sequence[Mapping[str, str]]:
  opts['format'] = '{{json .}}'
  res = docker('images', args, opts)
  return [
    cast(json.loads(_), Mapping[str, str])
    for _ in res.stdout.strip().split('\n')
  ]

def rmi(enforce: bool = True, *args: str, **opts: Option) -> None:
  docker('rmi', args, opts, enforce=enforce)
