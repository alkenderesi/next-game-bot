"""Message template module."""

import os
import json
from typing import Union


def read_templates(template_dir: str = "templates") -> dict[str, Union[str, dict]]:
    """
    Reads in all templates in the templates directory.

    For markdown templates, the file name is used as the key (`str`) and the file contents
    as the value (`str`).

    For JSON templates, the file name is used as the key (`str`) and the JSON object as
    the value (`dict`).

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


TEMPLATES = read_templates()


def create_choices_message(games: list[str]) -> str:
    """
    Creates a message containing the game choices.

    Args:
        * games (`list[str]`): The game choices.

    Returns:
        * `str`: The formatted message containing the game choices.
    """

    return TEMPLATES["choices.md"].format(
        choices="\n".join(
            [TEMPLATES["choice.md"].format(choice=game) for game in games]
        )
    )


def create_status_message(waiting_usernames: list[str], ok_usernames: list[str]) -> str:
    """
    Creates a message containing the status of the users.

    Args:
        * waiting_usernames (`list[str]`): The usernames of the users who have not
        responded.
        * ok_usernames (`list[str]`): The usernames of the users who have responded.

    Returns:
        * `str`: The formatted message containing the status of the users.
    """

    ok_status = "\n".join(
        [
            TEMPLATES["user_status.md"].format(
                status_emoji=TEMPLATES["emojis.json"]["ok"], username=username
            )
            for username in ok_usernames
        ]
    )
    waiting_status = "\n".join(
        [
            TEMPLATES["user_status.md"].format(
                status_emoji=TEMPLATES["emojis.json"]["waiting"], username=username
            )
            for username in waiting_usernames
        ]
    )

    return TEMPLATES["status.md"].format(
        user_count=len(waiting_usernames) + len(ok_usernames),
        response_count=len(ok_usernames),
        status=f"{ok_status}\n{waiting_status}",
    )
