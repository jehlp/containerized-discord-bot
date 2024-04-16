# Not part of stdlib
from discord.ext import commands

class DiscordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_response(self, ctx, message):
        await ctx.send(message)

    async def log_event(self, message):
        print(message)