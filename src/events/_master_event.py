from discord.ext import commands

class DiscordEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_event(self, message):
        print(message)