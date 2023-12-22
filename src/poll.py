"""Poll module for the bot."""

import discord
import collections
import math


class GamePoll:
    """Class for handling game polls."""

    def __init__(self):
        self.participants: set[discord.Member] = set()
        self.submissions: dict[discord.Member, tuple[int, list[str]]] = {}
        with open("config/games.txt", "r") as game_config:
            self.games = game_config.read().splitlines()

    @property
    def participant_count(self) -> int:
        return len(self.participants)

    @property
    def submission_count(self) -> int:
        return len(self.submissions)

    @property
    def game_count(self) -> int:
        return len(self.games)

    def is_active(self) -> bool:
        """
        Checks whether the poll is active.

        Returns:
            * `bool`: Whether the poll is active.
        """

        return bool(self.participants)

    def is_complete(self) -> bool:
        """
        Checks whether the poll is complete.

        Returns:
            * `bool`: Whether the poll is complete.
        """

        return self.participant_count == self.submission_count

    def add_participants(self, participants: list[discord.Member]) -> None:
        """
        Adds participants to the poll.

        Args:
            * participants (`list[discord.Member]`): The participants to add.
        """

        self.participants.update(participants)

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

        self.submissions[message.author] = (self.submission_count, games)

        return games

    def results(self) -> dict[str, float]:
        """
        Calculates the results of the poll.

        Returns:
            * `dict[str, float]`: The results of the poll.
        """

        results = collections.defaultdict(float)

        for response_order, games in self.submissions.values():
            response_bonus = GamePoll.bonus_function(len(games), self.game_count)
            speed_bonus = GamePoll.bonus_function(
                self.participant_count - response_order, self.participant_count
            )

            for placement, game in enumerate(games):
                placement_bonus = GamePoll.bonus_function(
                    self.game_count - placement, self.game_count
                )

                results[game] += response_bonus + speed_bonus + placement_bonus

        return results

    def reset(self) -> None:
        """Resets the poll."""

        self.participants.clear()
        self.submissions.clear()

    def bonus_function(x: int, x_max: int) -> float:
        return math.log(x, x_max) if min(x, x_max) > 1 else 0
