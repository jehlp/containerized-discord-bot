import asyncio
import src.cog
import src.utils
from discord.ext import commands

# Function 'graceful_shutdown' placed outside Shutdown class if graceful shutdown 
# needs to be called from another place in the code
async def graceful_shutdown(bot):
    # Close external resources, in this case probably an aiohttp session
    if hasattr(bot, 'session') and not bot.session.closed:
        await bot.session.close()
    # Cancel tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    await bot.close()

class Shutdown(src.cog.DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.shutdown_role = src.utils.get_shutdown_role()

    @commands.command(name='shutdown')
    async def command(self, ctx):
        if src.utils.has_role(ctx.author, self.shutdown_role):
            await ctx.send('Shutting down... 👋')
            await graceful_shutdown(self.bot)
        else:
            await ctx.send(f'You do not have the required role: {self.shutdown_role}')

    def help(self):
        return f"Shuts down the bot. Requires role {self.shutdown_role}."

async def setup(bot):
    await bot.add_cog(Shutdown(bot))