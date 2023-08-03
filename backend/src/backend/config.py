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


def get_configs(config_path: Path) -> Tuple[AppConfig, ScenarioConfig]:
    """_summary_

    Args:
        config_path (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        Tuple[AppConfig, ScenarioConfig]: _description_
    """
    json_config = read_json(config_path)
    return AppConfig(**json_config, config_path=config_path), ScenarioConfig(
        **json_config
    )
