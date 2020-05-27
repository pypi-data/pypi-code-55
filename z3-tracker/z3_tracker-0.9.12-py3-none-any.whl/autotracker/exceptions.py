'''
Exceptions for autotracker operation
'''


__all__ = 'AutotrackerException', 'NoConnection', 'ParseError', 'NoDevice'


class AutotrackerException(Exception):
    '''
    Base autotracker exception class.
    '''


class NoConnection(AutotrackerException):
    '''
    Raised when no connection could be established.
    '''


class ParseError(AutotrackerException):
    '''
    Raised when malformed server reply is encountered.
    '''

    
class NoDevice(AutotrackerException):
    '''
    Raised when chosen device is not found.
    '''
