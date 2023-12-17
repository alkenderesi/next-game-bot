"""Poll module for the bot."""

import discord
import json


class GamePoll:
    """Singleton class for handling game polls."""

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        with open("config/games.json", "r") as game_config:
            self.games: dict[str, str] = json.load(game_config)
        self.participants: list[discord.Member] = []
        self.submission: list[str] = []

    def is_active(self) -> bool:
        """Returns whether a game poll is active."""

        return bool(self.participants)
