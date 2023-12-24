"""Bot logic module."""

import discord


class PollBot():
    """Discord bot for poll creation and management."""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client: discord.Client) -> None:
        self.client = client

    async def message_handler(self, message: discord.Message) -> None:
        """
        Handles messages sent to the bot.

        Args:
            * message (`discord.Message`): The message sent to the bot.
        """

        pass
