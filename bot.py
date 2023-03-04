import discord #importing py-cord
from discord.ext import commands #importing commands
from dotenv import load_dotenv #importing load_dotenv from dotenv
import os #importing os

load_dotenv() #load the .env file

intents = discord.Intents.all() #setting intents, in this case i've set it to discord.Intents.all() so all intents are enabled
client = commands.Bot(command_prefix='!', intents=intents) #setting the client value, this especially prefix and intents

@client.event #making a new event decorator
async def on_ready(): #checking when the bot is started
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} | ID: {bot.user.id}") #telling what is the bot's user information

    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} guilds safe.") #defining the activity variable
    await bot.change_presence(status=discord.Status.online, activity=activity) #setting the status aswell as activity

client.load_extension('verification') #loading the verification cog

client.run(os.getenv('TOKEN')) #running the bot using the token stored in the .env file
