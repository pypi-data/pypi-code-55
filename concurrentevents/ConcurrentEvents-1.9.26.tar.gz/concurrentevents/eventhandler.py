from concurrentevents import _base
from concurrentevents._exceptions import Cancel


class EventHandler:
    """
    The main class used to implement a function to handle an event

    This is not required to handle function but rather standardizes useful
    functionality to simplify implementation

    Args:
        :param `**kwargs`: Keyword arguments used to set member variables
    """
    def __init__(self, **kwargs):
        """Constructor Method"""
        for keyword, arg in kwargs.items():
            setattr(self, keyword, arg)

        for var in dir(self):
            func = getattr(self, var)
            if hasattr(func, 'event'):
                # Replace the function object that catch put into handlers with the method object
                func.unload()
                _base.handlers[func.event].append(func)

    @staticmethod
    def fire(event):
        """
        Wrapper function for the event manager fire function

        Allows for function under an implemented event handler class to fire new events

        Args:
            :param event: A event to be fired through the event manager
            :type event: class:`concurrentevents.Event`
        """
        _base.event_manager.fire(event)

    def cancel(self):
        """
        A shortcut function to raise the cancel error signaling the __handler function to stop
        :raises Cancel: This error is a shortcut to trigger changes in the handling of an event
        """
        raise Cancel()
