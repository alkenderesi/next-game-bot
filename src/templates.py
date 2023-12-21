"""Message templating module."""

import os


def _safe_read(filename: str) -> str:
    with open(filename) as file:
        return file.read().strip()


TEMPLATE_DIR = "templates"
TEMPLATE_FILE_EXTENSION = ".md"
TEMPLATES = {
    filename[: -len(TEMPLATE_FILE_EXTENSION)]: _safe_read(f"{TEMPLATE_DIR}/{filename}")
    for filename in os.listdir(TEMPLATE_DIR)
    if filename.endswith(TEMPLATE_FILE_EXTENSION)
}


def options_message(options: list[str]) -> str:
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


def progress_message(answer_count: int, participant_count: int) -> str:
    """
    Creates a message containing the progress of the poll.

    Args:
        * answer_count (`int`): The number of answers received.
        * participant_count (`int`): The number of participants.

    Returns:
        * `str`: The formatted message containing the progress of the poll.
    """

    return TEMPLATES["progress"].format(
        answer_count=answer_count,
        participant_count=participant_count,
    )


def confirmation_message(confirmed_options: list[str]) -> str:
    """
    Creates a message containing the confirmed options.

    Args:
        * confirmed_options (`list[str]`): The confirmed options.

    Returns:
        * `str`: The formatted message containing the list of confirmed options.
    """

    return (
        TEMPLATES["confirmation"].format(
            confirmation_count=len(confirmed_options),
            confirmed_options="\n".join(
                [f"{i+1}. {option}" for i, option in enumerate(confirmed_options)]
            ),
        )
        if confirmed_options
        else TEMPLATES["confirmation"].format(
            confirmation_count=0,
            confirmed_options="https://youtu.be/QFgcqB8-AxE?si=fyW4ZChXoLb_F2so",
        )
    )


def results_message(results: dict[str, float]) -> str:
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
