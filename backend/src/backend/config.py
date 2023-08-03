import os
from pathlib import Path
from typing import Tuple

from pydantic import BaseModel, model_validator

from backend.utils import read_json


class ScenarioConfig(BaseModel, extra="ignore"):
    """Typed configuration class containing scenario configuration"""

    autonomy: int
    departure: str
    arrival: str


class AppConfig(BaseModel, extra="ignore"):
    """Typed configuration class containing application configuration"""

    config_path: Path
    routes_db: str

    @property
    def full_routes_db(self) -> Path:
        """Returns the full path to routes DB"""
        return self.config_path.parent / self.routes_db

    @model_validator(mode="after")
    def routes_db_must_exists(self) -> "AppConfig":
        """Validator ensuring database file existence.

        Raises:
            ValueError: raised if the target is not a file

        Returns:
            AppConfig: the application configuration
        """
        if not self.full_routes_db.is_file():
            raise ValueError(
                f"routes_db must exists and be a file: {self.full_routes_db}"
            )
        return self


def get_configs() -> Tuple[AppConfig, ScenarioConfig]:
    """Read and parse configuration file at CONFIG_PATH into file configuration

    Raises:
        ValueError: raised if CONFIG_PATH is not set, or does not point to a correct file

    Returns:
        Tuple[AppConfig, ScenarioConfig]: the configurations
    """
    config_path = os.getenv("CONFIG_PATH")
    if not config_path:
        raise ValueError("CONFIG_PATH env value should be set to config path")
    path = Path(config_path)
    json_config = read_json(path)
    return AppConfig(**json_config, config_path=path), ScenarioConfig(**json_config)
