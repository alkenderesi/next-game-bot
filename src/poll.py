"""Poll module for the bot."""

import discord


class GamePoll:
    """Class for handling game polls."""

    def __init__(self, participants: list[discord.Member]):
        self.participants = frozenset(participants)
        self.submissions: dict[discord.Member, tuple[int, list[str]]] = {}
        with open("config/games.txt", "r") as game_config:
            self.games = game_config.read().splitlines()

    def submit(self, message: discord.Message) -> list[str]:
        """
        Submits a response to the poll.

        Args:
            * message (`discord.Message`): The message to submit.

        Returns:
            * `list[str]`: The list of games in the order they were found in the
              message.
        """

        game_indices = {
            idx: game
            for game in self.games
            if (idx := message.content.find(game)) != -1
        }

        games = [game_indices[idx] for idx in sorted(game_indices.keys())]

        self.submissions[message.author] = (len(self.submissions), games)

        return games
