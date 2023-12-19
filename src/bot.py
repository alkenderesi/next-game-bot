"""Bot logic module."""

import discord
import templates
from poll import GamePoll


game_poll = GamePoll()
status_message: discord.Message = None


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
            print("Starting poll")
            game_poll.add_participants(message.mentions)
            await update_status_message(game_poll, message.channel)
            await message_participants(game_poll)

    # Handle private commands while a game poll is active
    elif message.channel.type.name == "private" and game_poll.is_active():
        pass


async def message_participants(game_poll: GamePoll) -> None:
    """
    Sends a message to all participants in the game poll.

    Args:
        * game_poll (`GamePoll`): The game poll.

    Raises:
        * ValueError: If the game poll is not active.
    """

    # Check whether the poll is active
    if not game_poll.is_active():
        raise ValueError("Game poll is not active.")

    # Build the message with the game choices
    message_content = templates.create_choices_message(game_poll.games)

    # Send the message to all participants
    for participant in game_poll.participants:
        print(f"Sending message to {participant.name}")
        await participant.send(message_content)


async def update_status_message(
    game_poll: GamePoll, channel: discord.TextChannel = None
) -> None:
    """
    Updates the status message with the current game poll status.

    If there is no status message, it will send a new one.

    Args:
        * game_poll (`GamePoll`): The game poll.
        * channel (`discord.TextChannel`, optional): The channel to send the initial status
        message to. Defaults to None.

    Raises:
        * AttributeError: If the channel is not set and there is no status message to update.
    """

    global status_message

    # Check whether the status message update can be performed
    if status_message is None and channel is None:
        raise AttributeError("Channel is not set.")

    # Build the message with the current poll status
    message_content = templates.create_status_message(
        waiting_usernames=[user.name for user in game_poll.participants],
        ok_usernames=[response.author.name for response in game_poll.responses],
    )

    # Set the channel to send the message to
    channel = channel or status_message.channel

    # Update the status message
    print("Updating status message")
    status_message = await channel.send(message_content)
