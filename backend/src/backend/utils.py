import json
from pathlib import Path
from typing import Any

from fastapi import UploadFile


def read_json(path: Path, encoding="utf-8") -> Any:
    """Read the file at path, et parse it as json

    Args:
        path (Path): path to the file
        encoding (str, optional): _description_. Defaults to "utf-8".

    Returns:
        Any: the json de-serialized
    """
    return json.loads(path.read_text(encoding=encoding))


async def read_json_file(json_file: UploadFile) -> Any:
    """Parse the given file and close it

    Args:
        json_file (UploadFile): the file to read

    Returns:
        Any: the json de-serialized
    """
    try:
        data = await json_file.read()
        return json.loads(data)
    finally:
        await json_file.close()
