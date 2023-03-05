import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verification_role: discord.Role = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_verification_role(self, ctx: commands.Context, role: discord.Role):
        self.verification_role = role
        await ctx.send(f"Verification role set to {role.name}.")

    @commands.command()
    async def send_verification(self, ctx: commands.Context):
        if self.verification_role is None:
            await ctx.send("Verification role not set.")
            return

        if self.verification_role in ctx.author.roles:
            await ctx.send("You have already been verified.")
            return

        embed = discord.Embed(title="Verification", description="Click the button below to verify!", color=discord.Color.green())
        button = discord.ui.Button(label="Verify", style=discord.ButtonStyle.green)
        view = discord.ui.View()
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return

            await interaction.response.send_message("You have been verified!", ephemeral=True)
            member = ctx.guild.get_member(interaction.user.id)
            await member.add_roles(self.verification_role)

            await interaction.message.delete()

            dm_channel = await interaction.user.create_dm()
            await dm_channel.send("You have been verified!")

        button.callback = button_callback

        await ctx.message.delete()
        await ctx.send(embed=embed, view=view, delete_after=10)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Verification(bot))
