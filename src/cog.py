# Not part of stdlib
from discord.ext import commands

class DiscordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Disable the default help command
        self.bot.help_command = None

    async def send_response(self, ctx, content=None, embed=None):
        return await ctx.send(content=content, embed=embed)

    async def log_event(self, message):
        print(message)

    def help(self):
        # If not overwritten, default 'help' is N/A
        return "No help available for this command."