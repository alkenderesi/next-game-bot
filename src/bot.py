"""Bot logic module."""

import discord
from poll import GamePoll


game_poll = GamePoll()


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

    # Handle public commands with the right prefix
    if message.channel.type.name == "text" and message.content.startswith("!nextgame"):
        pass

    # Handle private commands while a game poll is active
    elif message.channel.type.name == "private" and game_poll.is_active():
        pass
