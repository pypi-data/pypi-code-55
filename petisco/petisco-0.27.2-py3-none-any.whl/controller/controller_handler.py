import inspect
import traceback

from functools import wraps
from typing import Callable, Tuple, Dict, List, Any
from meiga import Result, Error, Success
from meiga.decorators import meiga
from petisco.application.petisco import Petisco
from petisco.controller.errors.internal_http_error import InternalHttpError
from petisco.controller.errors.known_result_failure_handler import (
    KnownResultFailureHandler,
)

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher
from petisco.events.request_responded import RequestResponded
from petisco.frameworks.flask.flask_headers_provider import flask_headers_provider
from petisco.logger.interface_logger import ERROR, INFO, DEBUG
from petisco.controller.errors.http_error import HttpError
from petisco.security.token_manager.not_implemented_token_manager import (
    NotImplementedTokenManager,
)
from petisco.security.token_manager.token_manager import TokenManager
from petisco.logger.log_message import LogMessage
from petisco.tools.timer import timer

DEFAULT_SUCCESS_MESSAGE = {"message": "OK"}, 200
DEFAULT_ERROR_MESSAGE = HttpError().handle()
DEFAULT_APP_NAME = "app-undefined"
DEFAULT_APP_VERSION = "version-undefined"
DEFAULT_LOGGER = None
DEFAULT_PUBLISHER = None


class _ControllerHandler:
    def __init__(
        self,
        app_name: str = DEFAULT_ERROR_MESSAGE,
        app_version: str = DEFAULT_APP_VERSION,
        logger=DEFAULT_LOGGER,
        token_manager: TokenManager = NotImplementedTokenManager(),
        success_handler: Callable[[Result], Tuple[Dict, int]] = None,
        error_handler: Callable[[Result], HttpError] = None,
        headers_provider: Callable = flask_headers_provider,
        logging_types_blacklist: List[Any] = [bytes],
        publisher: IEventPublisher = DEFAULT_PUBLISHER,
        send_request_responded_event: bool = False,
    ):
        """
        Parameters
        ----------
        app_name
            Application Name. If not specified it will get it from Petisco.get_app_version().
        app_version
            Application Version. If not specified it will get it from Petisco.get_app_version().
        logger
            A ILogger implementation. If not specified it will get it from Petisco.get_logger(). You can also use NotImplementedLogger
        token_manager
            TokenManager object. Here, you can define how to deal with JWT Tokens
        success_handler
            Handler to deal with Success Results
        error_handler
            Handler to deal with Failure Results
        headers_provider
            Injectable function to provide headers. By default is used headers_provider
        logging_types_blacklist
            Logging Blacklist. Object of defined Type will not be logged. By default ( [bytes] ) bytes object won't be logged.
        publisher
            A IEventPublisher implementation. If not specified it will get it from Petisco.get_event_publisher().
        send_request_responded_event
            Boolean to select if RequestResponded event is send. It will use provided publisher
        """
        self.app_name = app_name
        self.app_version = app_version
        self.logger = logger
        self.publisher = publisher
        self.token_manager = token_manager
        self.success_handler = success_handler
        self.error_handler = error_handler
        self.headers_provider = headers_provider
        self.logging_types_blacklist = logging_types_blacklist
        self.send_request_responded_event = send_request_responded_event

    def _check_app_name(self):
        if self.app_name == DEFAULT_ERROR_MESSAGE:
            self.app_name = Petisco.get_app_name()

    def _check_app_version(self):
        if self.app_version == DEFAULT_APP_VERSION:
            self.app_version = Petisco.get_app_version()

    def _check_logger(self):
        if self.logger == DEFAULT_LOGGER:
            self.logger = Petisco.get_logger()

    def _check_publisher(self):
        if self.publisher == DEFAULT_PUBLISHER:
            self.publisher = Petisco.get_event_publisher()

    def _configure_petisco_dependencies(self):
        self.petisco = Petisco.get_instance()
        self._check_app_name()
        self._check_app_version()
        self._check_logger()
        self._check_publisher()

    def _get_success_message(self, result: Result):
        message = ""
        if isinstance(result.value, tuple(self.logging_types_blacklist)):
            message = f"Success result of type: {type(result.value).__name__}"
        else:
            message = f"{result}"
        return message

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            @timer
            @meiga
            def run_controller(*args, **kwargs) -> Tuple[Result, float]:
                params = inspect.getfullargspec(func).args
                kwargs = {k: v for k, v in kwargs.items() if k in params}
                return func(*args, **kwargs)

            self._configure_petisco_dependencies()

            info_id = None
            is_success = False
            elapsed_time = None
            try:
                kwargs = add_petisco(kwargs)
                kwargs = add_headers(kwargs)
                result_kwargs = add_info_id(kwargs)

                log_message = LogMessage(
                    layer="controller", operation=f"{func.__name__}"
                )
                if result_kwargs.is_failure:
                    http_response = self.handle_failure(log_message, result_kwargs)
                else:
                    kwargs, info_id = result_kwargs.value
                    log_message.info_id = info_id
                    self.logger.log(INFO, log_message.set_message("Processing Request"))

                    result_controller, elapsed_time = run_controller(*args, **kwargs)

                    if result_controller.is_failure:
                        http_response = self.handle_failure(
                            log_message, result_controller
                        )
                    else:
                        message = self._get_success_message(result_controller)
                        self.logger.log(DEBUG, log_message.set_message(message))
                        http_response = (
                            self.success_handler(result_controller)
                            if self.success_handler
                            else DEFAULT_SUCCESS_MESSAGE
                        )
                        is_success = True
            except Exception as e:
                log_message = LogMessage(
                    layer="controller", operation=f"{func.__name__}"
                )
                log_message.info_id = info_id if info_id else None
                message = f"Error {func.__name__}: {repr(e.__class__)} {e} | {traceback.format_exc()}"
                self.logger.log(ERROR, log_message.set_message(message))
                http_response = InternalHttpError().handle()

            if self.send_request_responded_event:

                request_responded = RequestResponded(
                    app_name=self.app_name,
                    app_version=self.app_version,
                    controller=f"{func.__name__}",
                    is_success=is_success,
                    http_response=http_response,
                    elapsed_time=elapsed_time,
                ).add_info_id(info_id)

                self.publisher.publish(request_responded)

            return http_response

        def add_headers(kwargs):
            headers = self.headers_provider()
            kwargs = dict(kwargs, headers=headers)
            return kwargs

        def add_petisco(kwargs):
            kwargs = dict(kwargs, petisco=self.petisco)
            return kwargs

        @meiga
        def add_info_id(kwargs) -> Result[Tuple[str, InfoId], Error]:
            headers = kwargs.get("headers", {})

            info_id = self.token_manager.execute(headers).unwrap_or_return()

            kwargs = dict(kwargs, info_id=info_id)
            return Success((kwargs, info_id))

        return wrapper

    def handle_failure(
        self, log_message: LogMessage, result: Result
    ) -> Tuple[dict, int]:
        self.logger.log(ERROR, log_message.set_message(f"{result}"))
        known_result_failure_handler = KnownResultFailureHandler(result)
        http_response = DEFAULT_ERROR_MESSAGE
        if not known_result_failure_handler.is_a_result_known_error:
            if self.error_handler:
                http_error = self.error_handler(result)

                if not issubclass(http_error.__class__, HttpError):
                    raise TypeError(
                        "Returned object from error_handler must be subclasses of HttpError"
                    )

                http_response = http_error.handle()
        else:
            http_response = known_result_failure_handler.http_error.handle()
        return http_response


controller_handler = _ControllerHandler
