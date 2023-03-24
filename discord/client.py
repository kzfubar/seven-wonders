import discord
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=681633844151189554))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name="test", description="test", guild=discord.Object(id=681633844151189554))
async def tester(msg):
    await msg.response.send_message("slash successful")

with open("discord/token.txt", "r") as r:
    token = r.read()

client.run(token)