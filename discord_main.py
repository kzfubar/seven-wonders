from discord_client.client import create_client

client = create_client()

with open("discord_client/token.txt", "r") as r:
    token = r.read()

client.run(token)