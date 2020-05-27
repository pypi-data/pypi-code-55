from flatten_dict import flatten
from copy import deepcopy
from dpath.util import get, set


def import_package(package):
    try:
        return __import__(package)
    except ImportError:
        return None


PATH_DESCRIPTIONS = [
    # google
    ['request_body', 'originalRequest', 'data', 'inputs', '*', 'rawInputs', '*', 'query'],
    ['request_body', 'originalRequest', 'data', 'inputs', '*', 'arguments', '*', 'rawText'],
    ['request_body', 'originalRequest', 'data', 'inputs', '*', 'arguments', '*', 'textValue'],
    ['request_body', 'result', 'resolvedQuery'],
    ['request_body', 'result', 'parameters', '*'],
    ['request_body', 'result', 'contexts', '*', 'parameters', '*'],

    # alexa
    ['event', 'request', 'intent', 'slots', '*', 'value'],
    ['event', 'session', 'attributes', '*'],
    ['response', 'sessionAttributes', '*'],

    # facebook
    ['entry', '*', 'messaging', '*', 'message', 'text'],

    # generic
    ['text'],
    ['intent', 'inputs', '*', 'value'],

    # line
    ['message', 'text'],

    # rasa
    ['text']
]


def redact(obj):
    scrubadub = import_package('scrubadub')
    redactor = getattr(scrubadub, 'clean')

    if not redactor:
        raise Warning('PII Redaction currently not supported.')
        return

    paths = flatten(obj)

    def matchPathWrapper(objPath):
        def matchPath(pathDesc):
            if len(pathDesc) != len(objPath):
                return False
            else:
                return all([
                    True if v == "*" or v == objPath[i]
                    else False
                    for i, v in enumerate(pathDesc)
                ])
        return matchPath

    def filterPaths(objPath):
        return any(map(matchPathWrapper(objPath), PATH_DESCRIPTIONS))

    matchedPaths = list(filter(filterPaths, paths))

    if len(matchedPaths) == 0: return obj

    cloned = deepcopy(obj)

    for p in matchedPaths:
        value = get(cloned, list(p))
        if type(value) is str:
            newVal = redactor(value)
            set(cloned, p, newVal)

    return cloned

