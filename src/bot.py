"""Bot logic module."""

import discord
import templates
from poll import GamePoll


class NextGameBot:
    """Discord bot for game poll creation and management."""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.game_poll = GamePoll()
        self.status_message: discord.Message = None

    async def message_handler(self, message: discord.Message) -> None:
        """
        Handles messages sent to the bot.

        Args:
            * message (discord.Message): The message sent to the bot.
        """

        # Ignore messages sent by the bot itself
        if message.author == self.client.user:
            return

        # Handle public commands with the right prefix
        if message.channel.type.name == "text" and message.content.startswith(
            "!nextgame"
        ):
            # Start a poll
            if not self.game_poll.is_active() and message.mentions:
                print("Starting poll")
                self.game_poll.add_participants(message.mentions)
                await self.update_status_message(message.channel)
                await self.message_participants()

        # Handle private commands
        elif message.channel.type.name == "private":
            # Delete private message history
            if message.content.startswith("!clear"):
                await self.clear_private_history(message.author)

            # Add message to the responses
            elif (
                self.game_poll.is_active()
                and message.author in self.game_poll.participants
            ):
                print(f"Response received from {message.author.name}")
                self.game_poll.add_response(message)
                await self.update_status_message()

                # TODO: Send the final results if all participants have responded

    async def message_participants(self) -> None:
        """
        Sends a message to all participants in the game poll.

        Raises:
            * ValueError: If the game poll is not active.
        """

        # Check whether the poll is active
        if not self.game_poll.is_active():
            raise ValueError("Game poll is not active.")

        # Build the message with the game choices
        message_content = templates.create_choices_message(self.game_poll.games)

        # Send the message to all participants
        for participant in self.game_poll.participants:
            print(f"Sending choices to {participant.name}")
            await participant.send(message_content)

    async def update_status_message(self, channel: discord.TextChannel = None) -> None:
        """
        Updates the status message with the current game poll status.

        If there is no status message, it will send a new one.

        Args:
            * channel (`discord.TextChannel`, optional): The channel to send the initial status
            message to. Defaults to None.

        Raises:
            * AttributeError: If the channel is not set and there is no status message to update.
        """

        # Check whether the status message update can be performed
        if self.status_message is None and channel is None:
            raise AttributeError("Channel is not set.")

        # Build the message with the current poll status
        message_content = templates.create_status_message(
            waiting_usernames=[user.name for user in self.game_poll.participants],
            ok_usernames=[
                response.author.name for response in self.game_poll.responses
            ],
        )

        # Send or update the status message
        if channel:
            print("Sending initial status message")
            self.status_message = await channel.send(message_content)
        else:
            print("Updating status message")
            await self.status_message.edit(content=message_content)

    async def clear_private_history(self, member: discord.Member) -> None:
        """
        Clears the private message history with the given member.

        Args:
            * member (`discord.Member`): The member to clear the private message history with.
        """

        # Iterate through the member's private message history
        print(f"Clearing private message history for {member.name}")
        async for message in member.dm_channel.history():
            # Delete messages sent by the bot
            if message.author == self.client.user:
                await message.delete()
