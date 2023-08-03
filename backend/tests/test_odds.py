from backend.odds import compute_odds
from tests.conftest import ExampleScenario


def test_odds(scenario: ExampleScenario):
    odds = compute_odds(scenario.routes, scenario.scenario_config, scenario.scenario)
    print(odds)
    print(scenario.answer)
    assert (odds - scenario.answer) < 1e-2
