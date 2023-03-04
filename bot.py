import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

client.load_extension('main')

client.run('YOUR_TOKEN_HERE')
