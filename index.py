import os
os.system("pip install py-cord pytz python-dotenv")
import pytz
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)
utc = pytz.timezone('UTC')

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}#{client.user.discriminator}")

@client.event
async def on_guild_join(guild):
    owner = guild.owner
    embed = discord.Embed(title="Thanks for adding me to your server!", description="I'm here to help you be protected from pings.", color=discord.Color.green())
    try:
        await owner.send(embed=embed)
    except Exception as e:
        print(e)

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    if message.mentions:
        delete_time = datetime.now(utc)
        unix_timestamp = int(delete_time.timestamp())

        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            if entry.user == message.author:
                message_time = message.created_at.astimezone(utc)

                time_diff = delete_time - message_time

                if time_diff < timedelta(minutes=5):
                    embed = discord.Embed(title="Ghost Ping Detected!", color=discord.Color.red())
                    embed.add_field(name="User:", value=message.author.mention, inline=False)
                    embed.add_field(name="Message:", value=message.content, inline=False)
                    embed.add_field(name="Deleted on:", value=f"<t:{unix_timestamp}:R>", inline=False)
                    await message.channel.send(embed=embed)
                    break

client.run(TOKEN)
