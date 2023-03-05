import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}#{client.user.discriminator} | ID: {client.user.id}")

    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} guilds safe.")
    await client.change_presence(status=discord.Status.online, activity=activity)

client.load_extension('verification')

client.run(TOKEN)
