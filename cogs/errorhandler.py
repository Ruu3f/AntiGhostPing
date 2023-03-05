import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond('You are missing a required argument.')
        elif isinstance(error, commands.BadArgument):
            await ctx.respond('One or more of your arguments were invalid.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.respond('That command does not exist.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.respond('You do not have permission to run this command.')
        else:
            print(f'Unhandled error: {type(error).__name__}: {error}')

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
