import math
from dataclasses import dataclass
from logging import getLogger
from typing import Dict, List, Tuple

from backend.config import ScenarioConfig
from backend.data_contract import Scenario

LOGGER = getLogger(__name__)


def nb_encounter_to_odds(nb_encounter: int) -> float:
    """Compute the odds based of the number of encounter.

    Args:
        nb_encounter (int): the number of encounter

    Returns:
        float: the odds of arriving without being stopped
    """
    # The mathematical formula to compute the total probability of being captured is:
    # 1/10 + 9/10^2 + 9^2/10^3 + ... 9^k/10^(k+1)
    return sum((9 ^ k) / (10 ^ (k + 1)) for k in range(0, nb_encounter, 1))


@dataclass(frozen=True)
class Stage:
    """Data object representing a stage on itinerary"""

    planet: str
    cost: int


@dataclass(frozen=True)
class Itinerary:
    """Dataclass containing a "solution" to join destination"""

    stages: Tuple[Stage]

    @property
    def last_planet(self) -> str:
        """Shortcut to get the last planet name.

        Returns:
            str: the planet name
        """
        return self.stages[-1].planet

    def cost(self, autonomy: int) -> int:
        """Computes the naive way the cost of a solution

        Args:
            autonomy (int): the autonomy of the space ship

        Returns:
            int: the cost of the travel (may be infinity if unreachable)
        """
        leftover = autonomy
        cost = 0
        for stage in self.stages:
            # Check if planet is reachable
            # If not, then cost is inf
            if stage.cost > autonomy:
                cost = math.inf
                break
            cost += stage.cost
            # Check is next hop can be done without refuel
            if stage.cost <= leftover:
                leftover -= stage.cost
            # Else refuel
            else:
                leftover = autonomy
                cost += 1
        return cost

    def optimize_encounters(self, autonomy: int, scenario: Scenario) -> int:
        """Compute the minimum possible encounters for a working itinerary.
        It will optimize the odds, while respecting the maximum cost (ie countdown ).

        Args:
            autonomy (int): the autonomy of the spaceship
            scenario (Scenario): the scenario we compute against

        Returns:
            int: the minimum number of encounters
        """
        stack = [(0, 0, autonomy, 0)]
        bh_positions = scenario.view
        min_encounter = math.inf
        # Let's brute force for each solution, and keep best one
        while len(stack) > 0:
            nb_stage, nb_encounter, leftover, cost = stack.pop()
            current_planet = self.stages[nb_stage].planet
            # Let's check for bounty hunters
            if current_planet in bh_positions[cost]:
                nb_encounter += 1
            # Ignore inefficient solution
            if cost > scenario.countdown:
                continue
            # If we finished the travel, check the number of encounters
            if nb_stage == len(self.stages) - 1:
                min_encounter = min(min_encounter, nb_encounter)
                # We found optimal solution, we can stop
                if min_encounter == 0:
                    return 0
                # Let's search for better solution
                continue
            # Else, we need to continue the travel
            # We know solution is possible, so
            # - add a solution with a refuel
            next_stage = self.stages[nb_stage + 1]
            stack.append(
                (nb_stage + 1, nb_encounter, autonomy, cost + 1 + next_stage.cost)
            )
            # - try to go without refuel
            if next_stage.cost < leftover:
                stack.append(
                    (
                        nb_stage + 1,
                        nb_encounter,
                        autonomy - next_stage.cost,
                        cost + next_stage.cost,
                    )
                )
        return min_encounter


def compute_odds(
    routes: Dict[str, Dict[str, int]],
    scenario_config: ScenarioConfig,
    scenario: Scenario,
) -> float:
    """_summary_

    Args:
        routes (Dict[str, Dict[str, int]]): description of the "universe"
            (ie graph of planet with cost)
        scenario_config (ScenarioConfig): the scenario configuration
        scenario (Scenario): the scenario to estimate against

    Returns:
        float: the best odds
    """
    LOGGER.debug("Starting computing odds")
    LOGGER.debug(
        "Starting point: %s Destination: %s Autonomy: %s",
        scenario_config.departure,
        scenario_config.arrival,
        scenario_config.autonomy,
    )
    LOGGER.debug("Countdown: %s", scenario.countdown)
    LOGGER.debug("Hunters: %s", scenario.bounty_hunters)

    # First let's get all possible trajectory from the end to the start
    stack = [Itinerary([Stage(scenario_config.departure, 0)])]
    solutions: List[Tuple[int, Itinerary]] = []
    while len(stack) != 0:
        current = stack.pop()
        # Check if the cost is superior to countdown
        if current.cost(scenario_config.autonomy) > scenario.countdown:
            continue

        # If we arrive at destination, let's add it to solutions
        if current.last_planet == scenario_config.arrival:
            nb_encounter = current.optimize_encounters(
                scenario_config.autonomy, scenario
            )
            # Let's stop searching when found "optimal" solution
            if nb_encounter == 0:
                return 1.0
            solutions.append((nb_encounter, current))
            continue

        # Else let's go to other planets
        discovered = [s.planet for s in current.stages]
        for next_hop, cost in routes[current.last_planet].items():
            # Let's ensure we do no go twice to the same planet
            # NOTES(Bazire): Arguably, this could be needed to "dodge" bounty hunter in some cases
            # Should I remove it ?
            if next_hop in discovered:
                continue
            new_stages = list(current.stages) + [Stage(next_hop, cost)]
            stack.append(Itinerary(new_stages))

    # If no solutions if found, return 0
    if len(solutions) == 0:
        LOGGER.debug("No solution found")
        return 0.0

    # Else let's estimate each solution
    solutions.sort(key=lambda t: t[0])
    min_encounter, solution = solutions[0]
    odds = nb_encounter_to_odds(min_encounter)
    LOGGER.debug("Solution found with %s encounter, so % odds", min_encounter, odds)
    LOGGER.debug(solution)
    return odds
