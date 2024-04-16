from datetime import datetime

# Not part of stdlib
from discord.ext import commands

# Internal
from ..cog import DiscordCog

class Ping(DiscordCog):
    @commands.command(name='ping')
    async def command(self, ctx):
        start_time = datetime.now()
        message = await ctx.send('🏓 Pong!')
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds() * 1000
        await message.edit(content=f'🏓 Pong! Response time: {elapsed_time:.2f} ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))