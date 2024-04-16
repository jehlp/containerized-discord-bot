import discord
from discord.ext import commands

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(ping())

def ping():
    return "pong"

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
