import discord #importing py-cord
from discord.ext import commands #importing commands
from dotenv import load_dotenv #importing load_dotenv from dotenv
import os #importing os

load_dotenv() #load the .env file

intents = discord.Intents.all() #setting intents, in this case i've set it to discord.Intents.all() so all intents are enabled
client = commands.Bot(command_prefix='!', intents=intents) #setting the client value, this especially prefix and intents

@client.event #making a new event decorator
async def on_ready(): #checking when the bot is started
    print('Logged in as {0.user}'.format(client)) #telling what is the bot's user information

client.load_extension('verification') #loading the verification cog

client.run(os.getenv('TOKEN')) #running the bot using the token stored in the .env file
