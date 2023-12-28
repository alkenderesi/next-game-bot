import os


def safe_read(path: str) -> str:
    with open(path, "r") as file:
        content = file.read().strip()
    return content


DIR = "templates"
EXT = ".md"
TEMPLATES = {
    filename[: -len(EXT)]: safe_read(f"{DIR}/{filename}")
    for filename in os.listdir(DIR)
    if filename.endswith(EXT)
}


def poll_message(options: list[str]) -> str:
    return TEMPLATES["poll"].format(
        options="\n".join(
            [TEMPLATES["option"].format(option=option) for option in options]
        )
    )


def your_turn_message() -> str:
    return TEMPLATES["your_turn"]


def wait_message() -> str:
    return TEMPLATES["wait"]


def result_message(result: str) -> str:
    return TEMPLATES["result"].format(result=result)
