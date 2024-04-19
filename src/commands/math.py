# Not part of stdlib
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class Math(DiscordCog):
    @commands.command(name='math')
    async def command(self, ctx, *, equation: str = None):
        await ctx.send(content=f"{eval(equation)}")

    def help(self):
        return "Evaluates a string using python math"

async def setup(bot):
    await bot.add_cog(Math(bot))