import datetime
import src.cog
from discord.ext import commands

class Ping(src.cog.DiscordCog):
    @commands.command(name='ping')
    async def command(self, ctx):
        start_time = datetime.datetime.now()
        message = await ctx.send(content='🏓 Pong!')
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds() * 1000
        await message.edit(content=f'🏓 Pong! Response time: {elapsed_time:.2f} ms')

    def help(self):
        return "Test if the bot is responsive. If responsive, gives response time in ms."

async def setup(bot):
    await bot.add_cog(Ping(bot))