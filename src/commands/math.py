import math

# Not part of stdlib
import discord
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class Math(DiscordCog):
    @commands.command(name='math')
    async def command(self, ctx, *, equation: str = None):
        if equation:
            await ctx.send(content=f'Result: `{eval(equation)}`')
        else:
            await ctx.send(content='Please type a math equation!')

    def help(self):
        return "Evaluates a string using python math."

async def setup(bot):
    await bot.add_cog(Math(bot))