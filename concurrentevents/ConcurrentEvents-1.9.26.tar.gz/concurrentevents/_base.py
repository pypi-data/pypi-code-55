import logging

threads = None

event_manager = None

# Handler Dictionary,
#   key: Event Class Name
#   value: List of function objects
handlers = {}

log = logging.getLogger('__main__')

