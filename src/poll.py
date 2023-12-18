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
            self.games: list[str] = game_config.readlines()
        self.participants: set[discord.Member] = set()
        self.responses: list[list[str]] = []

    def is_active(self) -> bool:
        """Returns whether a poll is active."""

        return bool(self.participants)
