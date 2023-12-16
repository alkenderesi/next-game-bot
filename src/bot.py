"""Bot logic module."""

import discord
from poll import GamePoll


async def message_handler(message: discord.Message, client: discord.Client) -> None:
    """
    Handles messages sent to the bot.

    Args:
        * message (discord.Message): The message sent to the bot.
        * client (discord.Client): The Discord client.
    """

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
