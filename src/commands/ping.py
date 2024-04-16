# Not part of stdlib
from discord.ext import commands

# Internal
from ..cog import DiscordCog

class Ping(DiscordCog):
    @commands.command(name='ping')
    async def command(self, ctx):
        await self.send_response(ctx, 'pong')

async def setup(bot):
    await bot.add_cog(Ping(bot))