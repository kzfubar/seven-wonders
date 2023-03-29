import asyncio
import discord
import queue
from discord import app_commands
from discord_client.DiscordClient import DiscordClient

# guild=discord.Object(id=681633844151189554)

def create_client():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    players = {}

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        await tree.sync()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user = f'{message.author} | ID: {message.author.id}'

        if user not in players:
            return

        await players[user].receive_input(message.content)


    # Slash command to join game
    @tree.command(name="login", description="Join 7 Wonders Game")
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
            await interaction.user.send(f'```ansi\n{output}\n```')


    # Slash command to get help
    @tree.command(name="help", description="Shows game help commands and instructions")
    async def help(interaction):

        info = "Type /info to obtain board information on self and neighbors"
        wonders = "The seven available wonders are: Rhodos, Olympia, Gizah, Babylon, Alexandria, Halicarnassus, and Ephesus"
        pdf = "https://cdn.1j1ju.com/medias/c8/d6/88-7-wonders-rule.pdf"

        await interaction.user.send(f'```ansi\n{info}\n{wonders}\n{pdf}```')

    # Slash command to show players in lobby
    @tree.command(name="show_players", description="Show current players")
    async def show(interaction):
        await interaction.channel.send(players)

    
    return client