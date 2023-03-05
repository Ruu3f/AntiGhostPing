# import required libraries and modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# set the TOKEN variable to the value of the 'TOKEN' environment variable
TOKEN = os.getenv('TOKEN')

# create a new discord.Intents object with all intents enabled
intents = discord.Intents.all()

# create a new instance of the commands.Bot class with the command_prefix set to '!' and the intents set to the intents object
client = commands.Bot(command_prefix='!', intents=intents)

# define an async function called on_ready that is called when the bot is ready to start receiving events
@client.event
async def on_ready():
    # print a message to the console indicating that the bot has logged in and providing some information about the bot's user account
    print(f"Logged in as {client.user.name}#{client.user.discriminator} | ID: {client.user.id}")

    # create a new discord.Activity object with the type set to discord.ActivityType.watching and the name set to a string that includes the number of guilds (servers) the bot is a member of
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} guilds safe.")
    # call the client.change_presence() method to update the bot's presence in Discord. This sets the bot's status to online and its activity to the activity object created in the previous line.
    await client.change_presence(status=discord.Status.online, activity=activity)

# load a custom extension called 'verification'
client.load_extension('verification')

# call the client.run() method to start the bot and connect it to Discord using the TOKEN variable as the authentication key
client.run(TOKEN)
