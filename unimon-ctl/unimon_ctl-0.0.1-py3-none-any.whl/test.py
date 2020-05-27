from router import Router
from xenstore.xenstore import XenStore

xs = XenStore()

rtr = Router("test", xs, 44, "", 0)

print(rtr.get_state())
print(rtr.router_id)