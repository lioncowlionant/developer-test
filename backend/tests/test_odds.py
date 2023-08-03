from pathlib import Path
from typing import Dict

import pytest
import pytest_asyncio

from backend.config import ScenarioConfig
from backend.data_contract import Scenario
from backend.db import load_routes
from backend.odds import compute_odds
from backend.utils import read_json

ROOT_DATA_TEST = "/data/examples"


@pytest_asyncio.fixture(
    params=[p.name for p in Path(ROOT_DATA_TEST).iterdir() if p.is_dir()]
)
async def given_examples(request) -> Dict[str, Dict[str, int]]:
    base_path: Path = Path(ROOT_DATA_TEST) / request.param
    routes = await load_routes(base_path / "universe.db")
    scenario_config = ScenarioConfig(**read_json(base_path / "millennium-falcon.json"))
    scenario = Scenario(**read_json(base_path / "empire.json"))
    answer = read_json(base_path / "answer.json")["odds"]

    return routes, scenario_config, scenario, answer


def test_odds(given_examples):
    routes, scenario_config, scenario, answer = given_examples
    odds = compute_odds(routes, scenario_config, scenario)
    print(odds)
    print(answer)
    assert (odds - answer) < 1e-2
