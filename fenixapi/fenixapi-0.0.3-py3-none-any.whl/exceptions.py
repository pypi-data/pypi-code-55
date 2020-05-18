class LoginError(Exception):
    def __init__(self, message):
        super().__init__(message)

class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UndefinedError(Exception):
    def __init__(self, message):
        super().__init__(message)
