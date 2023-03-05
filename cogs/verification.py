import discord
from discord.ext import commands
from discord.commands import Option

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verification_role: discord.Role = None

    @commands.slash_command(name="set_vrole", description="Set the verification role.")
    @commands.has_permissions(administrator=True)
    async def set_vrole(self, ctx: commands.Context, role: Option(discord.Role, "The verification role.", required=True)):
        if role >= ctx.me.top_role:
            await ctx.respond("I cannot assign roles higher than or equal to my own.")
            return
        elif role >= ctx.author.top_role:
            await ctx.respond("You cannot assign roles higher than or equal to your own.")
            return

        self.verification_role = role
        embed = discord.Embed(description=f"Verification role set to {role.mention}.", color=0x2f3136)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="send_vembed", description="Send the verification embed.")
    @commands.has_permissions(administrator=True)
    async def send_vembed(self, ctx: commands.Context):
        if self.verification_role is None:
            embed = discord.Embed(description="Verification role not set.", color=0x2f3136)
            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(title="Verification", description="Click the button below to verify!", color=discord.Color.green())
        button = discord.ui.Button(label="Verify", style=discord.ButtonStyle.green)
        view = discord.ui.View(timeout=None)
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return
            if self.verification_role in ctx.author.roles:
                embed = discord.Embed(description="You have already been verified.", color=0x2f3136)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            embed = discord.Embed(description="You have been verified.", color=0x2f3136)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            member = ctx.guild.get_member(interaction.user.id)
            await member.add_roles(self.verification_role)

            dm_channel = await interaction.user.create_dm()
            await dm_channel.send(f"You have been verified in `{ctx.guild.name}`.")

        button.callback = button_callback

        await ctx.respond(embed=embed, view=view)

    @commands.slash_command(name="reset_vall", description="Reset all the verification settings.")
    @commands.has_permissions(administrator=True)
    async def reset_all(self, ctx: commands.Context):
        self.verification_role = None
        await ctx.respond("All verification settings have been reset.")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Verification(bot))
