# Not part of stdlib
from discord.ext import commands

# Internal
from ._master_command import DiscordCommand

class Ping(DiscordCommand):
    @commands.command(name='ping')
    async def command(self, ctx):
        await self.send_response(ctx, 'pong')

async def setup(bot):
    await bot.add_cog(Ping(bot))