import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

client.load_extension('verification')

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
print(f'DISCORD_TOKEN={DISCORD_TOKEN}')

client.run(DISCORD_TOKEN)
