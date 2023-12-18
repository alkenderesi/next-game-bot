"""Message template module."""

import os
import json
from typing import Union


def read_templates(template_dir: str = "templates") -> dict[str, Union[str, dict]]:
    """
    Reads in all templates in the templates directory.

    For markdown templates, the file name is used as the key (`str`) and the file contents as the value (`str`).

    For JSON templates, the file name is used as the key (`str`) and the JSON object as the value (`dict`).

    Args:
        * template_dir (`str`): The directory containing the templates.

    Returns:
        * `dict`: A dictionary containing all templates.
    """

    markdown_files = [file for file in os.listdir(template_dir) if file.endswith(".md")]
    json_files = [file for file in os.listdir(template_dir) if file.endswith(".json")]

    templates = {}

    for file in markdown_files:
        with open(f"{template_dir}/{file}") as f:
            templates[file] = f.read().strip()

    for file in json_files:
        with open(f"{template_dir}/{file}") as f:
            templates[file] = json.load(f)

    return templates
