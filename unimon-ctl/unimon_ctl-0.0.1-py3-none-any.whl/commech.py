class ComMechanism():

  ROUTER_STATUS = {
    "unknown": "can not determine router status",
    "running": "router is currently running",
    "stopped": "router is currently stopped",
    "error": "router has encountered an error"
  }

  def test(self, dom_id):
    raise NotImplementedError

  def get_type_name(self):
    ''' returns the name of the mech type '''
    return "Unknown Type"

  def get_router_state(self, dom_id, router_id):
    raise NotImplementedError

  def get_next_rid(self, dom_id):
    raise NotImplementedError

  def install_click_config(self, dom_id, config):
    ''' returns a router id on success, -1 on fail '''
    raise NotImplementedError

  def start_router(self, dom_id, router_id):
    ''' starts a router of a given id '''
    raise NotImplementedError

  def stop_router(self, dom_id, router_id):
    ''' stops a router of a given id '''
    raise NotImplementedError
