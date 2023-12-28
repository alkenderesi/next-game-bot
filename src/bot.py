import discord
import templates
from poll import Poll


class PollBot:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.poll = Poll()
        self.main_channel: discord.TextChannel = None
        self.poll_dms: dict[discord.Member, discord.Message] = {}
        self.turn_dms: dict[discord.Member, discord.Message] = {}

    async def message_handler(self, message: discord.Message) -> None:
        if message.author == self.client.user:
            return

        if (
            not self.poll.is_active()
            and not self.poll.is_complete()
            and message.channel.type.name == "text"
            and message.content.startswith("!nextgame")
            and message.mentions
            and self.client.user not in message.mentions
        ):
            await self.start(message)

        elif (
            self.poll.is_active()
            and message.channel.type.name == "private"
            and message.author == self.poll.active_participant
            and message.content in self.poll.games
        ):
            await self.submit(message)

        if self.poll.is_complete():
            await self.main_channel.send(templates.result_message(self.poll.result()))
            self.reset()

    async def start(self, message: discord.Message) -> None:
        self.poll.add(message.mentions)
        self.main_channel = message.channel

        poll_message = templates.poll_message(self.poll.games)
        your_turn_message = templates.your_turn_message()
        wait_message = templates.wait_message()

        for participant in self.poll.participants:
            dm_channel = await participant.create_dm()

            async for dm in dm_channel.history(limit=10, oldest_first=False):
                if dm.author == self.client.user:
                    await dm.delete()

            self.poll_dms[participant] = await participant.send(poll_message)

            if participant == self.poll.active_participant:
                self.turn_dms[participant] = await participant.send(your_turn_message)
            else:
                self.turn_dms[participant] = await participant.send(wait_message)

    async def submit(self, message: discord.Message):
        last_active = self.poll.active_participant
        self.poll.submit(message.content)

        poll_message = templates.poll_message(self.poll.games)
        your_turn_message = templates.your_turn_message()
        wait_message = templates.wait_message()

        await self.turn_dms[last_active].edit(content=wait_message)
        await self.turn_dms[self.poll.active_participant].edit(
            content=your_turn_message
        )

        for participant in self.poll.participants:
            await self.poll_dms[participant].edit(content=poll_message)

    def reset(self):
        self.poll.reset()
        self.main_channel = None
        self.poll_dms.clear()
        self.turn_dms.clear()
