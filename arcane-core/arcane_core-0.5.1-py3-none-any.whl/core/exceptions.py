from google.cloud import exceptions


GOOGLE_EXCEPTIONS_TO_RETRY = (
    exceptions.InternalServerError,
    exceptions.ServerError,
    exceptions.ServiceUnavailable,
    exceptions.GatewayTimeout,
    ConnectionResetError  # not a Google exception but can happen
)
