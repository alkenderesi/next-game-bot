"""Bot logic module."""

import discord
from templates import read_templates
from poll import GamePoll


TEMPLATES = read_templates()
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
        # Start a poll if one is not active and command has mentions
        if not game_poll.is_active() and message.mentions:
            game_poll.add_participants(message.mentions)
            await message_participants(game_poll)
            # TODO: Send poll status to public channel

    # Handle private commands while a game poll is active
    elif message.channel.type.name == "private" and game_poll.is_active():
        pass


async def message_participants(game_poll: GamePoll) -> None:
    """Sends a message to all participants in the game poll."""

    # Build the message with the game choices
    message = TEMPLATES["choices.md"].format(
        choices="\n".join(
            [TEMPLATES["choice.md"].format(choice=game) for game in game_poll.games]
        )
    )

    # Send the message to all participants
    for participant in game_poll.participants:
        await participant.send(message)
