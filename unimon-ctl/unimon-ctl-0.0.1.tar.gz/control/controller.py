from commech import ComMechanism
from xenstore import XenStore
import logging

class UnimonControl():

  VERSION = "0.01"
  DEFAULT_COM_MECH="xenstore"

  COMMUNICATION_MECHANISMS = {
    "xenstore": XenStore
  }

  def __init__(self, logger):
    self.logger = logger

  def update_logger(self, logger):
    self.logger = logger

  def __valid_mechanism(self, mech_name, dom_id):
    mech_name = mech_name.lower()
    if not mech_name in self.COMMUNICATION_MECHANISMS:
      self.logger.error("invalid communication mechanism given")
      return None
    try:
      mech = self.COMMUNICATION_MECHANISMS.get(mech_name)()
      if mech.test(dom_id):
        return mech
    except:
      self.logger.error("failed to create communication mechanism")
    return None

  def get_router_state(self, mechanism, domain_id, router_id):
    mechanism = self.__valid_mechanism(mechanism, domain_id)
    if not mechanism:
      return None
    return mechanism.get_router_state(domain_id, router_id)

  # def get_router_state(self, mechanism, domain_id, router_id):
  #   mechanism = self.__valid_mechanism(mechanism, domain_id)
  #   if not mechanism:
  #     return None
  #   return mechanism.get_router_state(domain_id, router_id)

  def start_router(self, mechanism, domain_id, config_path):
    mechanism = self.__valid_mechanism(mechanism, domain_id)
    if not mechanism:
      return None
    try:
      with open(config_path, 'r') as config_file:
        config = config_file.read()
        rid = mechanism.install_click_config(domain_id, config)
        if not rid:
          self.logger.error("could not install config")
          return None
        return rid
    except:
      self.logger.error("config file could not be read")
      return None