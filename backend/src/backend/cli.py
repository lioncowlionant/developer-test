from pathlib import Path

import anyio
import typer
from typing_extensions import Annotated

from backend.config import get_configs
from backend.data_contract import Scenario
from backend.db import load_routes
from backend.odds import compute_odds
from backend.utils import read_json


def what_are_the_odds(
    config_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the configuration file (ie millennium-falcon.json)"
        ),
    ],
    scenario_path: Annotated[
        Path, typer.Argument(help="Path to the scenario file (ie empire.json)")
    ],
):
    """Compute the odds of the given scenario against the given configuration.

    Raises:
        ValueError: raised if scenario file is not a file.
    """
    app_config, scenario_config = get_configs(config_path)
    # Run asynchronous code synchronously
    routes = anyio.run(load_routes, app_config.full_routes_db)
    if not scenario_path.is_file():
        raise ValueError("scenario_path must be a json file with proper format")
    scenario = Scenario(**read_json(scenario_path))
    odds = compute_odds(
        routes=routes, scenario_config=scenario_config, scenario=scenario
    )
    print(odds)
    return odds


if __name__ == "__main__":
    typer.run(what_are_the_odds)
