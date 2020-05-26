class ODRouteException(BaseException):
    pass

class ODRouteConfigException(ODRouteException):
    pass

class PortAlreadyUsed(ODRouteException):
    pass
