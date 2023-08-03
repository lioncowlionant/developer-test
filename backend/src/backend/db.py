from collections import defaultdict
from pathlib import Path
from typing import Dict

import aiosqlite
from pydantic import BaseModel, ConfigDict

ROUTES_TABLE = "ROUTES"


class Route(BaseModel):
    """Basic model used to parse and validate data from database"""

    model_config = ConfigDict(alias_generator=str.lower, extra="forbid")

    origin: str
    destination: str
    travel_time: int


async def load_routes(db_path: Path) -> Dict[str, Dict[str, int]]:
    """Loads all possible routes into a dict origin => destination => travel_time

    Args:
        db_path (Path): the path to the SQLlite db

    Returns:
        Dict[str, Dict[str, int]]: the routes dict [origin => [destination => travel_time]]
    """
    routes: Dict[str, Dict[str, int]] = defaultdict(dict)
    async with aiosqlite.connect(db_path) as db_connection:
        db_connection.row_factory = aiosqlite.Row
        async with db_connection.execute(f"SELECT * FROM {ROUTES_TABLE}") as cursor:
            async for row in cursor:
                # Using Pydantic to validate and format data
                route = Route(**dict(row))
                routes[route.origin][route.destination] = route.travel_time
                routes[route.destination][route.origin] = route.travel_time
    return routes
