import logging
from lura.run import RunResult, run
from typing import List, Mapping, Optional, Sequence, Union

log = logging.getLogger(__name__)

#####
## helpers

class settings:

  docker_compose_bin: str = 'docker-compose'
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
      raise ValueError(
        f'Invalid value for docker-compose argument {name}: {value} ({type(value)})')
    return f'--{name}' if value is None else f'--{name}={value}'

  return tuple(
    opt
    for opt in (convert_opt(name, val) for (name, val) in opts.items())
    if opt is not None
  )

#####
## docker-compose

def docker_compose(
  cmd: str,
  file: Optional[str] = None,
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  cwd: str = None
) -> RunResult:
  argv: List[str] = [settings.docker_compose_bin]
  if file:
    argv.extend(('-f', file))
  argv.append(cmd)
  argv.extend(args)
  argv.extend(convert_opts(opts))
  with run.log(log, settings.log_level):
    return run(argv, cwd=cwd)

def pull(
  file: Optional[str] = None,
  cwd: Optional[str] = None,
  *args: str,
  **opts: Option
) -> None:
  docker_compose('pull', file, args, opts, cwd)
