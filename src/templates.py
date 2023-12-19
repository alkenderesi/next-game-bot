"""Message templating module."""

import os
import json
from typing import Union


def read_templates(template_dir: str = "templates") -> dict[str, Union[str, dict]]:
    """
    Reads in all templates in the templates directory.

    For markdown templates, the filename is used as the key (`str`) and the file contents as the value (`str`).

    For JSON templates, the filename is used as the key (`str`) and the JSON object as the value (`dict`).

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
            templates[file[: -len(".md")]] = f.read().strip()

    for file in json_files:
        with open(f"{template_dir}/{file}") as f:
            templates[file[: -len(".json")]] = json.load(f)

    return templates


TEMPLATES = read_templates()


def create_options_message(options: list[str]) -> str:
    """
    Creates a message containing the list of options.

    Args:
        * options (`list[str]`): The options to vote on.

    Returns:
        * `str`: The formatted message containing the list of options.
    """

    return TEMPLATES["options"].format(
        options="\n".join(
            [TEMPLATES["option"].format(option=option) for option in options]
        )
    )


def create_status_message(ok_usernames: list[str], waiting_usernames: list[str]) -> str:
    """
    Creates a message containing the status of the users.

    Args:
        * ok_usernames (`list[str]`): The usernames of the users who have responded.
        * waiting_usernames (`list[str]`): The usernames of the users who have not responded.

    Returns:
        * `str`: The formatted message containing the status of the users.
    """

    status = ""

    if ok_usernames:
        status += (
            "\n".join(
                [
                    TEMPLATES["user_status"].format(
                        status_emoji=TEMPLATES["emojis"]["ok"], username=username
                    )
                    for username in ok_usernames
                ]
            )
            + "\n"
        )

    if waiting_usernames:
        status += "\n".join(
            [
                TEMPLATES["user_status"].format(
                    status_emoji=TEMPLATES["emojis"]["waiting"], username=username
                )
                for username in waiting_usernames
            ]
        )

    return TEMPLATES["status"].format(
        user_count=len(waiting_usernames) + len(ok_usernames),
        response_count=len(ok_usernames),
        status=status,
    )


def create_feedback_message(confirmed_options: list[str]) -> str:
    """
    Creates a message containing the confirmed options.

    Args:
        * confirmed_options (`list[str]`): The confirmed options.

    Returns:
        * `str`: The formatted message containing the list of confirmed options.
    """

    feedback = "\n".join(
        [f"{i+1}. {option}" for i, option in enumerate(confirmed_options)]
    )

    return TEMPLATES["feedback"].format(
        feedback_count=len(confirmed_options), feedback=feedback
    )


def create_results_message(results: dict[str, float]) -> str:
    """
    Creates a message containing the results of the poll.

    Args:
        * results (`dict[str, float]`): The results of the poll.

    Returns:
        * `str`: The formatted message containing the results of the poll.
    """

    return "\n".join(
        [
            TEMPLATES["result"].format(
                score=f"{score:.2f}".rjust(5),
                option=option,
            )
            for option, score in sorted(
                results.items(), key=lambda item: item[1], reverse=True
            )
        ]
    )
