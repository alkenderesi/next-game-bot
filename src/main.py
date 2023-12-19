"""Main module that runs the bot."""

import discord
import bot


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
next_game_bot = bot.NextGameBot(client)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    await next_game_bot.message_handler(message)


def main():
    with open("config/token.txt", "r") as token_file:
        TOKEN = token_file.read().strip()

    client.run(TOKEN)


if __name__ == "__main__":
    main()
