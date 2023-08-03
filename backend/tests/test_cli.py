from backend.cli import what_are_the_odds
from backend.utils import read_json
from tests.conftest import ExampleFolderStructure


def test_cli(scenario_paths: ExampleFolderStructure):
    answer = read_json(scenario_paths.answer_path)["odds"]

    odds = what_are_the_odds(scenario_paths.config_path, scenario_paths.scenario_path)
    print(odds)
    print(answer)
    assert odds == answer
