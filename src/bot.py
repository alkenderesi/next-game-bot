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
        self.info_message: discord.Message = None

    async def message_handler(self, message: discord.Message) -> None:
        """
        Handles messages sent to the bot.

        Args:
            * message (`discord.Message`): The message sent to the bot.
        """

        if message.author == self.client.user:
            return

        if (
            not self.game_poll.is_active()
            and message.channel.type.name == "text"
            and message.content.startswith("!nextgame")
            and message.mentions
        ):
            await self._start_poll(message)

        elif (
            self.game_poll.is_active()
            and message.channel.type.name == "private"
            and message.author in self.game_poll.participants
            and message.author not in self.game_poll.submissions
        ):
            await self._submit_poll_response(message)

            if self.game_poll.is_complete():
                await self._end_poll()

    async def _start_poll(self, message: discord.Message) -> None:
        """
        Starts a new poll.

        This includes sending the initial progress message to the main channel,
        clearing the private message history with all the participants,
        and sending the game options to them.

        Args:
            * message (`discord.Message`): The message sent to the bot with the
              participants of the poll.
        """

        self.game_poll.add_participants(message.mentions)

        self.info_message = await message.channel.send(
            templates.progress_message(0, self.game_poll.participant_count)
        )

        for participant in self.game_poll.participants:
            dm_channel = await participant.create_dm()
            async for dm in dm_channel.history():
                if dm.author == self.client.user:
                    await dm.delete()

            await participant.send(templates.options_message(self.game_poll.games))

    async def _submit_poll_response(self, message: discord.Message) -> None:
        """
        Submits a response to the poll.

        This includes sending a confirmation message to the participant,
        and updating the progress message in the main channel.

        Args:
            * message (`discord.Message`): The message sent to the bot with the
              participant's response.
        """

        await message.channel.send(
            templates.confirmation_message(self.game_poll.submit(message))
        )

        await self.info_message.edit(
            content=templates.progress_message(
                self.game_poll.submission_count, self.game_poll.participant_count
            )
        )

    async def _end_poll(self) -> None:
        """
        Ends the poll.

        This includes updating the info message in the main channel with the results of
        the poll, and resetting the poll.
        """

        await self.info_message.edit(
            content=templates.results_message(self.game_poll.results())
        )

        self.game_poll.reset()
