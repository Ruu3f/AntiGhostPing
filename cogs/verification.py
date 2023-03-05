import os
import discord
from discord.ext import commands
from discord.commands import Option

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verification_role = self.file_path = None

    async def set_reset_vrole(self, ctx: commands.Context, role=None, reset=False):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond('You do not have permissions to perform this action')

        if role and (role >= ctx.me.top_role or role >= ctx.author.top_role):
            return await ctx.respond('I cannot assign roles higher than or equal to my own.')

        if not self.verification_role and reset is False:
            return await ctx.respond('Verification role not set.')

        if role:
            self.verification_role = role
            with open(self.file_path, "w") as f:
                f.write(f"{ctx.guild.id}:{role.id}")
            await ctx.send(embed=discord.Embed(description=f"Verification role set to {role.mention}.", color=0x2f3136))
        else:
            self.verification_role = None
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    line = f.read()
                    if line:
                        guild_id, role_id = line.split(":")
                        guild = self.bot.get_guild(int(guild_id))
                        role = guild.get_role(int(role_id))
                        if role:
                            await role.delete()
                os.remove(self.file_path)
            await ctx.respond("All verification settings have been reset.")

    @commands.slash_command(name="set_vrole", description="Set the verification role.")
    async def set_vrole(self, ctx: commands.Context, role: Option(discord.Role, "The verification role.", required=True)):
        await self.set_reset_vrole(ctx, role=role)

    @commands.slash_command(name="reset_vall", description="Reset all the verification settings.")
    async def reset_all(self, ctx: commands.Context):
        await self.set_reset_vrole(ctx, reset=True)

    @commands.slash_command(name="send_vembed", description="Send the verification embed.")
    async def send_vembed(self, ctx: commands.Context):
        if self.verification_role is None:
            return await ctx.respond('Verification role not set.')

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

def setup(bot: commands.Bot):
    bot.add_cog(Verification(bot))
