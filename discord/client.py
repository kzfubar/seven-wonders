import discord
from discord import app_commands
from DiscordClient import DiscordClient


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

players = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=681633844151189554))

# test
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(f'{message.author}: Hello!')

# Slash command to join game
@tree.command(name="login", description="Join 7 Wonders Game", guild=discord.Object(id=681633844151189554))
async def login(interaction):
    user = f'{interaction.user} | ID: {interaction.user.id}'
    
    user_input = queue.Queue()
    user_output = queue.Queue()

    user_client = DiscordClient(user_input, user_output)

    players[user] = user_client

    
# Slash command to show players in lobby
@tree.command(name="show_players", description="Show current players", guild=discord.Object(id=681633844151189554))
async def show(interaction):
    await interaction.channel.send(players)

with open("discord/token.txt", "r") as r:
    token = r.read()

client.run(token)


