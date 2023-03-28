import asyncio
import discord
import queue
from discord import app_commands
from discord_client.DiscordClient import DiscordClient

def create_client():
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

        user = f'{message.author} | ID: {message.author.id}'

        if user not in players:
            return

        await players[user].receive_input(message.content)


    # Slash command to join game
    @tree.command(name="login", description="Join 7 Wonders Game", guild=discord.Object(id=681633844151189554))
    async def login(interaction):
        user = f'{interaction.user} | ID: {interaction.user.id}'
        
        user_output = queue.Queue()

        user_client = DiscordClient(user_output)

        players[user] = user_client
        asyncio.create_task(user_client.start(interaction.user.name)) 

        while True:
            while user_output.empty():
                await asyncio.sleep(1)

            output = user_output.get()
            print(output)
            await interaction.user.send(output)


    # Slash command for help commands
    @tree.command(name="help", description="Show available commands", guild=discord.Object(id=681633844151189554))
    async def help(interaction):
        
        info = "Type /info to obtain board information "

        
    # Slash command to show players in lobby
    @tree.command(name="show_players", description="Show current players", guild=discord.Object(id=681633844151189554))
    async def show(interaction):
        await interaction.channel.send(players)

    
    return client