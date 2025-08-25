"""Application configuration."""

import os
from typing import cast

import yaml

from py4ai.core.config import merge_confs, joinPath, path_constructor, env_var_matcher
from py4ai.core.config.configurations import BaseConfig, FileSystemConfig

yaml.add_implicit_resolver("!path", env_var_matcher)
yaml.add_constructor("!path", path_constructor)
yaml.add_constructor("!joinPath", joinPath)


class StorageConfig(BaseConfig):
    """Storage configuration object."""

    @property
    def fs(self) -> FileSystemConfig:
        """
        Get File System configuration.

        :return: FileSystemConfig
        """
        return FileSystemConfig(self.sublevel("fs"))


class LogConfig(BaseConfig):
    """Log configuration object."""

    @property
    def file(self) -> str:
        """
        Get file with logging configurations.

        :return: path to file
        """
        return cast(str, self.getValue("file"))

    @property
    def defaults(self) -> str:
        """
        Get file with default logging configurations.

        :return: path to file
        """
        return cast(str, self.getValue("defaults"))


class APIConfig(BaseConfig):
    """API configuration object."""

    @property
    def port(self) -> int:
        """
        Return port of webserver.

        :return: webserver port
        """
        return cast(int, self.config["port"])

    @property
    def host(self) -> str:
        """
        Return host of webserver.

        :return: webserver host
        """
        return cast(str, self.config["host"])


class AppConfig(BaseConfig):
    """Application configuration object."""

    @property
    def storage(self) -> StorageConfig:
        """
        Get storage config.

        :return: storage config
        """
        return StorageConfig(self.sublevel("storage"))

    @property
    def log(self) -> LogConfig:
        """
        Get log config.

        :return: storage config
        """
        return LogConfig(self.sublevel("log"))

    @property
    def api(self) -> APIConfig:
        """
        Get the API config.

        :return: API config
        """
        return APIConfig(self.sublevel("api"))


__conf_dir__ = os.path.join(os.environ["PROJECT_DIR"], "config")
__conf_file__ = os.path.join(__conf_dir__, f"app.{os.environ['ENV']}.yml")

config = AppConfig(
    config=merge_confs(
        filenames=[__conf_file__],
        default=os.path.join(__conf_dir__, "defaults.yml"),
    )
)
