import json
from pathlib import Path
from typing import Any


def read_json(path: Path, encoding="utf-8") -> Any:
    """Read the file at path, et parse it as json

    Args:
        path (Path): path to the file
        encoding (str, optional): _description_. Defaults to "utf-8".

    Returns:
        Any: the json de-serialized
    """
    return json.loads(path.read_text(encoding=encoding))
