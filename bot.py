# import required libraries and modules
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# install required libraries
os.system("pip install py-cord python-dotenv")

# load the .env file
load_dotenv()

# get the token from the environment variables
TOKEN = os.getenv('TOKEN')

# create a new instance of the commands.Bot class with the command_prefix set to '!' and the intents set to all the intents
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

# event that triggers when the bot is ready
@client.event
async def on_ready():
    # print a message to the console indicating that the bot has logged in and providing some information about the bot's user account
    print(f"Logged in as {client.user.name}#{client.user.discriminator} | ID: {client.user.id}")

    # create a new discord.Activity object with the type set to discord.ActivityType.watching and the name set to a string that includes the number of guilds (servers) the bot is a member of
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} guilds safe.")

    # call the client.change_presence() method to update the bot's presence in Discord. This sets the bot's status to online and its activity to the activity object created in the previous line.
    await client.change_presence(status=discord.Status.online, activity=activity)

# load the cogs
client.load_extension('cogs.verification')
client.load_extension('cogs.errorhandler')

# run the bot
client.run(TOKEN)
