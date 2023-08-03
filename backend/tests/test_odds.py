import pytest

from backend.odds import compute_odds, nb_encounter_to_odds
from tests.conftest import ExampleScenario


def test_compute_odds(scenario: ExampleScenario):
    odds = compute_odds(scenario.routes, scenario.scenario_config, scenario.scenario)
    print(odds)
    print(scenario.answer)
    assert odds == scenario.answer


@pytest.mark.parametrize(
    "nb_encounter,expected_odds",
    [
        (0, 1.0),
        (1, 0.9),
        (2, 0.81),
        (3, 0.729),
    ],
)
def test_nb_encounter_to_odds(nb_encounter, expected_odds):
    odds = nb_encounter_to_odds(nb_encounter)
    print(odds)
    print(expected_odds)
    assert odds == expected_odds
