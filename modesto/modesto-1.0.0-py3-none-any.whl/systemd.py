import logging
from lura.run import RunResult, run
from typing import List, Mapping, Optional, Sequence, Union

log = logging.getLogger(__name__)

#####
## helpers

class settings:

  systemctl_bin: str = 'systemctl'
  journalctl_bin: str = 'journalctl'
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
      raise ValueError(f'Invalid value for argument {name}: {value} ({type(value)})')
    return f'--{name}' if value is None else f'--{name}={value}'

  return tuple(
    opt 
    for opt in (convert_opt(name, val) for (name, val) in opts.items())
    if opt is not None
  )

#####
## systemctl functions

def systemctl(
  cmd: str,
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  enforce: bool = True,
  log_level: Optional[int] = None
) -> RunResult:

  argv: List[str] = [settings.systemctl_bin, cmd]
  argv.extend(args)
  argv.extend(convert_opts(opts))
  log_level = log_level if log_level is not None else settings.log_level
  with run.log(log, log_level):
    return run(argv, enforce=enforce)

def start(*args: str, **opts: Option) -> None:
  systemctl('start', args, opts)

def stop(*args: str, **opts: Option) -> None:
  systemctl('stop', args, opts)

def restart(*args: str, **opts: Option) -> None:
  systemctl('restart', args, opts)

def reload(*args: str, **opts: Option) -> None:
  systemctl('reload', args, opts)

def started(svc: str) -> None:
  return systemctl('status', [svc], {}, enforce=False).code == 0

def enable(*args: str, **opts: Option) -> None:
  systemctl('enable', args, opts)

def disable(*args: str, **opts: Option) -> None:
  systemctl('disable', args, opts)

def enabled(*args: str, **opts: Option) -> bool:
  return systemctl('is-enabled', args, opts, enforce=False).code == 0

def daemon_reload(*args: str, **opts: Option) -> None:
  systemctl('daemon-reload', args, opts)

#####
## journalctl functions

def journalctl(
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  log_level: Optional[int] = None
) -> RunResult:

  argv: MutableSequence[str] = [settings.journalctl_bin]
  argv.extend(args)
  argv.extend(convert_opts(opts))
  log_level = log_level or settings.log_level
  with run.log(log, log_level):
    return run(argv)

def journal(svc: str, *args: str, **opts: Option) -> str:
  opts['unit'] = svc
  return journalctl(args, opts).stdout

#####
## service wrapper

class Service:

  _name: str

  def __init__(self, name: str) -> None:
    super().__init__()
    self._name = name

  @property
  def name(self) -> str:
    return self._name

  @property
  def started(self) -> bool:
    return started(self._name)

  @property
  def stopped(self) -> bool:
    return not started(self._name)

  @property
  def enabled(self) -> bool:
    return enabled(self._name)
   
  @property
  def disabled(self) -> bool:
    return not enabled(self._name)

  def start(self) -> None:
    start(self._name)

  def stop(self) -> None:
    stop(self._name)

  def restart(self) -> None:
    restart(self._name)

  def reload(self) -> None:
    reload(self._name)

  def enable(self) -> None:
    enable(self._name)

  def disable(self) -> None:
    disable(self._name)

  def journal(self, *args: str, **opts: Option) -> str:
    return journal(self._name, *args, **opts)
