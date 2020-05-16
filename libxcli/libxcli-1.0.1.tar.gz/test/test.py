from xcommon import XClient


c = XClient.Xclient()

c.connect('127.0.0.1',10000)

c.close()
