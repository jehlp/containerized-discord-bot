# Not part of stdlib
import discord
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class DiscordHelp(commands.HelpCommand):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", description="List of all available commands:", color=discord.Color.blue())
        for cog, commands in mapping.items():
            if cog is not None and commands:
                command_list = [f"`{command.name}`: {cog.help()}" for command in commands]
                if command_list:
                    embed.add_field(name=cog.qualified_name, value="\n".join(command_list), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        help_text = command.cog.help()
        embed = discord.Embed(title=f"Help for `{command.name}`", description=help_text, color=discord.Color.green())
        await self.get_destination().send(embed=embed)

class Help(DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot.help_command = DiscordHelp(command_prefix=bot.command_prefix)

async def setup(bot):
    await bot.add_cog(Help(bot))