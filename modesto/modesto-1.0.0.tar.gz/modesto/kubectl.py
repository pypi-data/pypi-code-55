import io
import json
import logging
from abc import abstractmethod
from contextlib import contextmanager
from lura import fs
from lura.expanders import Jinja2
from lura.run import RunError, RunResult, run
from typing import (
  Any, Iterator, List, Mapping, NamedTuple, Optional, Sequence, Union
)

log = logging.getLogger(__name__)

#####
## helpers

class settings:

  kubectl_bin: str = 'kubectl'
  log_level: int = logging.DEBUG

Option = Union[str, int, float, bool, None]

def convert_opts(opts: Mapping[str, Option]) -> Sequence[str]:

  def convert_opt(name: str, value: Option) -> Optional[str]:
    name = name.replace('_', '-')
    if isinstance(value, (str, int, float)):
      value = str(value)
    elif isinstance(value, bool):
      value = 'true' if value else 'false'
    elif value is None:
      return None
    else:
      raise ValueError(f"Invalid value for kubectl argument {name}: {value} ({type(value)})")
    return f"--{name}={value}"

  return tuple(convert_opt(name, value) for name, value in opts.items())

#####
## kubectl functions

def kubectl(
  cmd: str,
  args: Sequence[str] = (),
  opts: Mapping[str, Option] = {},
  cwd: Optional[str] = None,
  enforce: bool = True,
) -> RunResult:

  argv = [settings.kubectl_bin, cmd]
  argv.extend(args)
  argv.extend(convert_opts(opts))
  with run.log(log, settings.log_level):
    return run(argv, cwd=cwd, enforce=enforce)

def get(*args: str, **opts: Option) -> Mapping[str, Any]:
  opts['output'] = 'json'
  return json.loads(kubectl('get', args, opts).stdout)

def apply(*args: str, **opts: Option) -> None:
  kubectl('apply', args, opts)

def delete(*args: str, enforce: bool = True, **opts: Option) -> None:
  kubectl('delete', args, opts, enforce=enforce)

def diff(*args: str, **opts: Option) -> str:
  return kubectl('diff', args, opts).stdout

def applied(**opts: Option) -> bool:
  return kubectl('diff', (), opts).code == 0

def logs(*args: str, **opts: Option) -> str:
  return kubectl('logs', args, opts).stdout

#####
## pod wrapper

class Pod:

  @classmethod
  def select(
    cls,
    selector: str,
    namespace: Optional[str] = None
  ) -> Sequence['Pod']:
    'Return pods that match `selector` as a sequence of `Pod` objects.'

    pods = get('pod', selector=selector, namespace=namespace)
    return tuple(
      cls(pod['metadata']['name'], namespace)
      for pod in pods['items']
    )

  _name: str
  _namespace: Optional[str]

  def __init__(self, name: str, namespace: Optional[str] = None) -> None:
    super().__init__()
    self._name = name
    self._namespace = namespace

  @property
  def name(self) -> str:
    return self._name

  @property
  def namespace(self) -> str:
    return self._namespace

  @property
  def running(self) -> bool:
    # FIXME use pod status
    try:
      pod = get('pod', self._name, namespace=self._namespace)
      return True
    except RunError:
      return False

  def journal(self, count: int) -> str:
    return logs(self._name, namespace=self._namespace, tail=count)

#####
## resource wrapper

class Resource:

  @property
  @abstractmethod
  def body(self) -> str:
    return ''

  @property
  def applied(self) -> bool:
    with self.file() as path:
      applied(filename=path)

  @abstractmethod
  @contextmanager
  def file(self) -> Iterator[str]:
    yield ''

  def apply(self) -> None:
    with self.file() as path:
      apply(filename=path)

  def delete(self) -> None:
    with self.file() as path:
      delete(filename=path)

class ResourceString(Resource):

  _body: str

  def __init__(self, body: str) -> None:
    super().__init__()
    self._body = body

  @property
  def body(self) -> str:
    return self._body

  @contextmanager
  def file(self) -> Iterator[str]:
    with fs.TempDir(prefix=f'{__name__}.') as temp_dir:
      path = f'{temp_dir}/resource.yaml'
      fs.dumps(path, self.body)
      yield path

class ResourceTemplate(ResourceString):

  def __init__(self, template: str, env: Mapping[Any, Any]) -> None:
    body = Jinja2().expands(template, env)
    super().__init__(body)

class ResourceFile(Resource):

  _path: str

  def __init__(self, path: str) -> None:
    super().__init__()
    self._path = path

  @property
  def body(self) -> str:
    return fs.loads(self._path)

  @contextmanager
  def file(self) -> Iterator[str]:
    yield self._path

#####
## application wrapper

class Application:

  _name: str
  _resources: Sequence[Resource]

  def __init__(self, name: str, resources: Sequence[Resource]) -> None:
    super().__init__()
    self._name = name
    self._resources = resources

  @property
  def name(self) -> str:
    return self._name

  @property
  def applied(self) -> bool:
    return all(resource.applied for resource in self._resources)

  @property
  def manifest(self) -> str:
    with io.StringIO() as buf:
      for resource in self._resources:
        buf.write('---\n')
        buf.write(resource.body.rstrip())
        buf.write('\n')
      return buf.getvalue()

  def apply(self) -> None:
    log.info(f'Applying {self._name}')
    for resource in self._resources:
      resource.apply()

  def delete(self) -> None:
    log.info(f'Deleting {self._name}')
    for resource in self._resources:
      resource.delete()
