from suanpan import api, g

g.apiHost = "10.88.36.254"
g.debug = True

print(api.call(32430, "test", {"x": 1, "y": 2}))
