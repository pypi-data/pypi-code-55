class InputError(Exception):
    def __init__(self, index, input):
        message = input + b'<-'
        super(InputError, self).__init__(message)
