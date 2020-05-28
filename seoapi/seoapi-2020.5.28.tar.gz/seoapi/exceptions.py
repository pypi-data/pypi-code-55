# -*- coding: utf-8 -*-


class ApiError(Exception):
    def __init__(self, response, *args, **kwargs):
        super().__init__()
        self.response = response

    def __str__(self):
        return f'{self.response.url}\n{self.response.headers}\n' \
            f'{self.response.status_code} {self.response.reason}\n' \
            f'{self.response.text}'


class ServerError(ApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RequestError(ApiError):
    def __init__(self, response, *args, **kwargs):
        super().__init__(response, *args, **kwargs)
        self.error = self.response.json()

    def __str__(self):
        return f'{self.response.url}\n{self.response.headers}\n' \
            f'{self.response.status_code} {self.response.reason}\n' \
            f'{self.error}'


class AuthError(RequestError):
    def __init__(self, response, *args, **kwargs):
        super().__init__(response, *args, **kwargs)

    def __str__(self):
        return f'Ошибка доступа, проверьте токен\n{self.error["error"]}'


class SessionDuplicateError(RequestError):
    def __init__(self, response, *args, **kwargs):
        super().__init__(response, *args, **kwargs)

    def __str__(self):
        return 'Такой идентификатор сессии уже существует'


class SessionNotExistError(RequestError):
    def __init__(self, response, *args, **kwargs):
        super().__init__(response, *args, **kwargs)

    def __str__(self):
        return 'Такой идентификатор сессии не существует'
