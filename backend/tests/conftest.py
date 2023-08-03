from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pytest
import pytest_asyncio

from backend.config import ScenarioConfig
from backend.data_contract import Scenario
from backend.db import load_routes
from backend.utils import read_json

ROOT_DATA_TEST = "/data/examples"


@dataclass
class ExampleFolderStructure:
    base_path: Path

    @property
    def db_path(self) -> Path:
        return self.base_path / "universe.db"

    @property
    def config_path(self) -> Path:
        return self.base_path / "millennium-falcon.json"

    @property
    def scenario_path(self) -> Path:
        return self.base_path / "empire.json"

    @property
    def answer_path(self) -> Path:
        return self.base_path / "answer.json"


@dataclass
class ExampleScenario:
    routes: Dict[str, Dict[str, int]]
    scenario_config: ScenarioConfig
    scenario: Scenario
    answer: float


@pytest.fixture(params=[p.name for p in Path(ROOT_DATA_TEST).iterdir() if p.is_dir()])
def scenario_paths(request):
    base_path: Path = Path(ROOT_DATA_TEST) / request.param
    return ExampleFolderStructure(base_path)


@pytest_asyncio.fixture
async def scenario(scenario_paths: ExampleFolderStructure) -> ExampleScenario:
    routes = await load_routes(scenario_paths.db_path)
    scenario_config = ScenarioConfig(**read_json(scenario_paths.config_path))
    scenario = Scenario(**read_json(scenario_paths.scenario_path))
    answer = read_json(scenario_paths.answer_path)["odds"]

    return ExampleScenario(routes, scenario_config, scenario, answer)
