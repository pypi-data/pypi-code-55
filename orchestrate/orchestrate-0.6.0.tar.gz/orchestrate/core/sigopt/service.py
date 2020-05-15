import six
from sigopt import Connection
from sigopt.exception import ApiException

from orchestrate.common import safe_format
from orchestrate.core.exceptions import CheckConnectionError
from orchestrate.core.services.base import Service


class SigOptService(Service):
  def __init__(self, services, api_token=None, api_url=None):
    super(SigOptService, self).__init__(services)
    self._api_token = api_token
    self._api_url = api_url

  @property
  def conn(self):
    try:
      conn = Connection(client_token=self._api_token)
      if self._api_url:
        conn.set_api_url(self._api_url)
      return conn
    except ValueError as ve:
      six.raise_from(
        ValueError("Must set environment variable SIGOPT_API_TOKEN"),
        ve,
      )

  @property
  def api_token(self):
    return self.conn.impl.requestor.auth.username

  @property
  def api_url(self):
    return self.conn.impl.api_url

  def check_connection(self):
    try:
      self.conn.experiments().fetch(limit=1)
    except ApiException as e:
      six.raise_from(
        CheckConnectionError(safe_format('An error occured while checking your SigOpt connection: {}'), str(e)),
        e,
      )

  def create_experiment(self, **kwargs):
    return self.conn.experiments().create(**kwargs)

  def fetch_experiment(self, experiment_id):
    return self.conn.experiments(experiment_id).fetch()

  def iterate_observations(self, experiment_id):
    return self.conn.experiments(experiment_id).observations().fetch().iterate_pages()

  def safe_fetch_experiment(self, experiment_id):
    try:
      return self.fetch_experiment(experiment_id)
    except ApiException as e:
      if e.status_code in [403, 404]:
        return None
      raise
