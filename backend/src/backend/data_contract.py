from collections import defaultdict
from typing import Dict, List

from pydantic import BaseModel


class BountyHunter(BaseModel, extra="forbid"):
    """Dataclass representing a bounty hunter"""

    planet: str
    day: int


class Scenario(BaseModel, extra="forbid"):
    """Dataclass representing a scenario to run"""

    countdown: int
    bounty_hunters: List[BountyHunter]

    @property
    def view(self) -> Dict[int, List[str]]:
        """Present the data in an easier way to use
            ie to check where bounty hunters are at a given date.

        Returns:
            Dict[int, List[str]]: a dict mapping the for each day the list
                of planets occupied by bounty hunters
        """
        table = defaultdict(list)
        for hunter in self.bounty_hunters:
            table[hunter.day].append(hunter.planet)
        return table
