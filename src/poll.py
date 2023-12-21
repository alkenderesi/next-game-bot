"""Poll module for the bot."""

import discord


class GamePoll:
    """Class for handling game polls."""

    def __init__(self, participants: list[discord.Member]):
        self.participants = frozenset(participants)
        self.submissions: dict[discord.Member, tuple[int, list[str]]] = {}
        with open("config/games.txt", "r") as game_config:
            self.games = game_config.read().splitlines()
