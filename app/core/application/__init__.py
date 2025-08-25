"""Application factory module."""

import datetime
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Type, TypeVar, Union, cast

from fastapi import APIRouter, FastAPI, Request, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from py4ai.core.logging import WithLogging

E = TypeVar("E", bound=Exception)


class FastAPIFactory(WithLogging, ABC):
    """Class implementing the application factory."""

    def __init__(
        self,
        uid: str,
        name: str,
        description: str = "",
        startup_timestamp: datetime.datetime = datetime.datetime.now(),
    ) -> None:
        """Initialize the FastAPIFactory class.

        :param uid: the unique identifier for the application.
        :param name: the name of the application.
        :param description: the description of the application.
        :param startup_timestamp: the startup timestamp for the application.
        """
        self.uid = uid
        self.name = name
        self.startup_timestamp = startup_timestamp
        self.app = FastAPI(
            title=f"Microservice [{uid}] - {self.name}", description=description
        )
        self._configure()
        self.configure_cors()
        self.configure_gzip()
        self.logger.info(
            f"Microservice [{self.uid}] - {self.name} "
            f"successfully initialized at {self.startup_timestamp}"
        )

    @abstractmethod
    def _configure(self) -> None:
        """Configure the microservice."""
        ...

    def configure_cors(self) -> None:
        """Register CORS for current application."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def configure_gzip(self) -> None:
        """Register GZip middleware for current application."""
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)

    def register_api_router(self, router: APIRouter) -> None:
        """Register a generic API Router.

        :param router: the router to be registered.
        """
        self.app.include_router(router)

    def register_error_handler(
        self,
        exception: Type[Exception],
        handler: Union[
            Callable[[Request, E], Union[Response, Awaitable[Response]]],
            Callable[[WebSocket, E], Awaitable[None]],
        ],
    ) -> None:
        """Register a generic handler for a specific exception type.

        :param exception: exception type to be handled.
        :param handler: the current handler to be used for the exception type.
        """
        self.app.add_exception_handler(
            exception,
            cast(
                Union[
                    Callable[
                        [Request, Exception], Union[Response, Awaitable[Response]]
                    ],
                    Callable[[WebSocket, Exception], Awaitable[None]],
                ],
                handler,
            ),  # This cast is required since starlette's add_exception_handler method is ill-typed
        )
