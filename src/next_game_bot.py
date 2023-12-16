import discord

with open("config/token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
