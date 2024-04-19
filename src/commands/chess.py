# Not part of stdlib
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class Chess(DiscordCog):
    @commands.command(name='chess')
    async def command(self, ctx):
        await ctx.send(content=f'Chess!')

    def help(self):
        return "Chess!"

async def setup(bot):
    await bot.add_cog(Chess(bot))