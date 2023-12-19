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

        if message.author == self.client.user:
            return

        if message.channel.type.name == "text":
            if (
                message.content.startswith("!nextgame")
                and not self.game_poll.is_active()
                and message.mentions
            ):
                await self.start_poll(message.mentions, message.channel)

        elif message.channel.type.name == "private":
            if message.content.startswith("!clear"):
                await self.clear_private_history(message.author)

            elif (
                self.game_poll.is_active()
                and message.author in self.game_poll.participants
            ):
                await self.save_poll_response(message)

                # TODO: Send the final results if all participants have responded

    async def message_participants(self) -> None:
        """Sends a message to all participants in the game poll."""

        message_content = templates.create_choices_message(self.game_poll.games)

        for participant in self.game_poll.participants:
            print(f"Sending choices to {participant.name}")
            await participant.send(message_content)

    async def update_status_message(self, channel: discord.TextChannel = None) -> None:
        """
        Updates the status message with the current game poll status.

        If there is no status message, it will send a new one.

        Args:
            * channel (`discord.TextChannel`, optional): The channel to send the initial
              status message to. Defaults to None.

        Raises:
            * AttributeError: If the channel is not set and there is no status message
              to update.
        """

        if self.status_message is None and channel is None:
            raise AttributeError("Channel is not set.")

        message_content = templates.create_status_message(
            [user.name for user in self.game_poll.participants],
            [response.author.name for response in self.game_poll.responses],
        )

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
            * member (`discord.Member`): The member to clear the private message history
              with.
        """

        print(f"Clearing private messages history for {member.name}")

        async for message in member.dm_channel.history():
            if message.author == self.client.user:
                await message.delete()

    async def start_poll(
        self, participants: list[discord.Member], status_channel: discord.TextChannel
    ) -> None:
        """
        Starts a new game poll.

        Args:
            * participants (list of `discord.Member`): The participants of the game
              poll.
            * status_channel (`discord.TextChannel`): The channel to send the status
              message to.
        """

        print("Starting poll")

        self.game_poll.add_participants(participants)
        await self.update_status_message(status_channel)
        await self.message_participants()

    async def save_poll_response(self, message: discord.Message) -> None:
        """
        Saves a response to the game poll.

        Args:
            * message (`discord.Message`): The response message to save.
        """

        print(f"Response received from {message.author.name}")

        self.game_poll.add_response(message)
        await self.update_status_message()
