"""Poll module for the bot."""

import discord


class GamePoll:
    """Singleton class for handling game polls."""

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        with open("config/games.txt", "r") as game_config:
            self.games: list[str] = game_config.read().splitlines()
        self.participants: set[discord.Member] = set()
        self.responses: list[discord.Message] = []

    def is_active(self) -> bool:
        """Returns whether a poll is active."""

        return bool(self.participants)

    def add_participants(self, participants: list[discord.Member]) -> None:
        """
        Adds participants to the poll.

        Args:
            * participants (`list[discord.Member]`): The list of participants.
        """

        self.participants.update(participants)

    def add_response(self, response: discord.Message) -> None:
        """
        Adds a response to the poll.

        Args:
            * response (`discord.Message`): The response to add.
        """

        self.participants.remove(response.author)
        self.responses.append(response)

    def get_results(self) -> dict[str, float]:
        """Returns the results of the poll."""

        pass

    def reset(self) -> None:
        """Resets the poll."""

        self.participants.clear()
        self.responses.clear()
