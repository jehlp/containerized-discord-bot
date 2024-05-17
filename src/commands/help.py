from discord import Color
from discord.ext import commands
from src.cog import DiscordCog
from src.utils.general import create_embed, split_camel_case

class Help(DiscordCog):
    @commands.command(name='help')
    async def command(self, ctx, command_name=None):
        if command_name:
            # User asked for help on a specific command
            command = self.bot.get_command(command_name)
            if command and command.cog:
                embed = create_embed(
                    title=f"Help for `{command.name}`", 
                    description=command.cog.help(),
                    color=Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(content=f"No command named `{command_name}` found.")
        else:
            # General help, list all commands
            embed = create_embed(
                title="Help", 
                description="List of all available commands:", 
                color=Color.blue()
            )
            # Sort commands alphabetically
            for cog_name, cog in sorted(self.bot.cogs.items(), key=lambda item: item[0]):
                command_list = [f"`{command.name}`: {cog.help()}" for command in cog.get_commands()]
                if command_list:
                    formatted_cog_name = split_camel_case(cog_name)
                    embed.add_field(name=formatted_cog_name, value="\n".join(command_list), inline=False)
            await ctx.send(embed=embed)

    def help(self):
        return "Use `!help` to get a list of all commands, or `!help <command>` for detailed help on a specific command."

async def setup(bot):
    await bot.add_cog(Help(bot))