import os
import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verification_role = None

    @commands.command(name="send_vembed", description="Send the verification embed.")
    async def send_vembed(self, ctx: commands.Context):
        if self.verification_role is None:
            await ctx.send('Verification role not set.')
            return

        embed = discord.Embed(title="Verification", description="Click the button below to verify!", color=discord.Color.green())
        button = discord.ui.Button(label="Verify", style=discord.ButtonStyle.green)
        view = discord.ui.View(timeout=None)
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author or self.verification_role in ctx.author.roles:
                return

            member = ctx.guild.get_member(interaction.user.id)
            await member.add_roles(self.verification_role)

            dm_channel = await interaction.user.create_dm()
            await dm_channel.send(f"You have been verified in `{ctx.guild.name}`.")

            await interaction.response.send_message(content="You have been verified.", ephemeral=True)

        button.callback = button_callback
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Verification(bot))
