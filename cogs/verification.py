import os
import discord
from discord.ext import commands


class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.verification_role = None
        self.file_path = "vroles.txt"

    async def cog_before_invoke(self, ctx: commands.Context):
        if self.verification_role is None:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    line = f.read()
                    if line:
                        guild_id, role_id = line.split(":")
                        guild = self.bot.get_guild(int(guild_id))
                        role = guild.get_role(int(role_id))
                        if role:
                            self.verification_role = role
                        else:
                            os.remove(self.file_path)
            else:
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                open(self.file_path, "w").close()

    async def cog_after_invoke(self, ctx: commands.Context):
        if self.verification_role:
            with open(self.file_path, "w") as f:
                f.write(f"{ctx.guild.id}:{self.verification_role.id}")

    @commands.command(name="send_vembed", description="Send the verification embed.")
    async def send_vembed(self, ctx: commands.Context):
        if self.verification_role is None:
            await ctx.send('Verification role not set.')
            return

        embed = discord.Embed(
            title="Verification",
            description="Click the button below to verify!",
            color=discord.Color.green()
        )
        button = discord.ui.Button(label="Verify", style=discord.ButtonStyle.green)
        view = discord.ui.View(timeout=None)
        view.add_item(button)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user != ctx.author:
                return

            if self.verification_role in ctx.author.roles:
                await interaction.response.send_message(
                    content="You have already been verified.",
                    ephemeral=True
                )
                return

            member = ctx.guild.get_member(interaction.user.id)
            await member.add_roles(self.verification_role)

            dm_channel = await interaction.user.create_dm()
            await dm_channel.send(f"You have been verified in `{ctx.guild.name}`.")

            await interaction.response.send_message(
                content="You have been verified.",
                ephemeral=True
            )

        button.callback = button_callback

        await ctx.send(embed=embed, view=view)

    @commands.command(name="set_vrole", description="Set the verification role.")
    async def set_vrole(self, ctx: commands.Context, role: discord.Role):
        if role and (role >= ctx.me.top_role or role >= ctx.author.top_role):
            await ctx.send('I cannot assign roles higher than or equal to my own.')
            return

        if role:
            self.verification_role = role
            with open(self.file_path, "w") as f:
                f.write(f"{ctx.guild.id}:{role.id}")
            await ctx.send(content=f"Verification role set to {role.mention}.")
        else:
            await ctx.send('Please provide a role.')

    @commands.command(name="reset_vall", description="Reset all the verification settings.")
    async def reset_all(self, ctx: commands.Context):
        self.verification_role = None
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                line = f.read()
                if line:
                    guild_id, role_id = line.split(":")
                    guild = self.bot.get_guild(int(guild_id))
                    role = guild.get_role(int(role_id))
                    if role:
                        os.remove(self.file_path)
                        await ctx.send("All verification settings have been reset.")
                        return
        await ctx.send('Verification settings file not found.')

def setup(bot):
    bot.add_cog(Verification(bot))
