# -*- coding: utf-8 -*-
from commech import ComMechanism
try:
  from pyxs import Client as PyXSClient
  from pyxs import PyXSError
except:
  print("UnimonCtl requires the pyxs package for xenstore communication")
import logging
import os


class XenStore(ComMechanism):

  DEFAULT_SOCKET_PATH = "/var/run/xenstored/socket"

  CLICKOS_BASE_PATH = "data/clickos"
  UNIMON_BASE_PATH = "/data/unimon"

  ENCODING = "utf-8"
  XS_CHUNK = 512
  MAX_TRIES = 3

  def __init__(self):
    logging.info("adding xenstore mechanism...")
    self.socket_path = os.getenv("XS_SOCKET", self.DEFAULT_SOCKET_PATH)
    logging.debug(" - using socket path %s" % self.socket_path)
    if not self.__test_connection():
      exit(1)
    logging.info("xenstore mechanism added ✅")

  def __test_connection(self):
    logging.debug("testing xenstore connection")
    client = PyXSClient(unix_socket_path=self.socket_path)
    try:
      client.connect()
    except PyXSError as e:
      logging.error("xenstore connection failed")
      return False
    finally:
      client.close()
    return True

  def __is_clickos(self, dom_id):
    base_path = self.__get_base_path(dom_id)
    if not base_path:
      return False
    with PyXSClient(unix_socket_path=self.socket_path) as client:
      if client.exists(base_path.encode(self.ENCODING)):
        return True
    logging.error("domain is not clickos")
    return False

  def __next_router_id(self, dom_id):
    base_path = self.__get_base_path(dom_id)
    if not base_path:
      return -1
    

  def __write_to_xs(self, dom_id, router_id, path_ext, value):
    base_path = self.__get_base_path(dom_id)
    if not base_path:
      return False
    path = "{}/{}/{}".format(base_path, str(router_id), path_ext)
    with PyXSClient(unix_socket_path=self.socket_path) as client:
      tries = 0
      while True:
        tries += 1
        tr_id = client.transaction()
        client.mkdir(path.encode(self.ENCODING))
        client.write(path.encode(self.ENCODING), value.encode(self.ENCODING))
        if client.commit():
          logging.debug("xenstore transaction (%d) complete" % tr_id)
          return True
        if tries == self.MAX_TRIES:
          logging.error("xenstore transaction (%d) failed" % tr_id)
          client.rollback()
          return False
    
  def __read_from_xs(self, dom_id, router_id, path_ext):
    base_path = self.__get_base_path(dom_id)
    if not base_path:
      return None
    path = "{}/{}/{}".format(base_path, str(router_id), path_ext)
    with PyXSClient(unix_socket_path=self.socket_path) as client:
      try:
        value = client.read(path.encode(self.ENCODING))
        logging.debug("xenstore read success")
      except PyXSError as e:
        value = None
        logging.error("xenstore read failed")
      finally:
        if value != None:
          return value.decode(self.ENCODING)
        else:
          return None

  def __get_base_path(self, dom_id):
    base_path = ""
    with PyXSClient(unix_socket_path=self.socket_path) as client:
      domain_path = (client.get_domain_path(dom_id)).decode(self.ENCODING)
      if not domain_path:
        logging.error("xenstore attempted to access domain with an invalid id")
        base_path = None
      else:
        base_path = "{}/{}".format(domain_path, self.CLICKOS_BASE_PATH)
    return base_path

  def __set_router_status(self, dom_id, router_id, status):
    if not status in self.ROUTER_STATUS:
      logging.error("attempted to set invalid router status via xenstore")
      return False
    written = self.__write_to_xs(dom_id, router_id, "status", status)
    if written:
      value = self.__read_from_xs(dom_id, router_id, "status")
      if value == status:
        logging.debug("|| status set | dom {} | rtr {} | status {} ||".format(dom_id, router_id, status))
        return True
    logging.error("failed to write router status")
    return False

  def test(self, dom_id):
    return (self.__test_connection() and self.__is_clickos(dom_id))

  def get_type_name(self):
    return "xenstore"

  def get_router_state(self, dom_id, router_id):
    return self.__read_from_xs(dom_id, router_id, "status")

  def get_next_rid(self, dom_id):
    base_path = self.__get_base_path(dom_id)
    if not base_path:
      return None
    try:
      with PyXSClient(unix_socket_path=self.socket_path) as client:
        raw_list = client.list(base_path.encode(self.ENCODING))
      routers = []
      for value in raw_list:
        value = value.decode(self.ENCODING)
        try:
          value = int(value)
          routers.append(value)
        except:
          continue
      return max(routers)
    except:
      logging.error("could not get list of routers for domain {}", dom_id)
    return None
    
  # def install_click_config(self, dom_id, router_id, config, config_name="unnamed configuration"):
  #   ''' returns a router id on success, -1 on fail '''
  #   try:
  #     with PyXSClient(unix_socket_path=self.socket_path) as client:
  #       i = 0
  #       while True:
  #         pos = (i * self.XS_CHUNK)
  #         if pos >= len(config):
  #           break
  #         path_ext = "config/{}".format(pos)
  #         self.__write_to_xs(dom_id, router_id, path_ext, config[pos:self.XS_CHUNK-1])

  
