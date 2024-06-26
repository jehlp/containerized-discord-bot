from src.cog import DiscordCog
from src.utils.general import get_shutdown_role, has_role
from src.utils.asynchronous import graceful_shutdown
from discord.ext import commands

class Shutdown(DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.shutdown_role = get_shutdown_role()

    @commands.command(name='shutdown')
    async def command(self, ctx):
        if has_role(ctx.author, self.shutdown_role):
            await ctx.send('Shutting down... 👋')
            await graceful_shutdown(self.bot)
        else:
            await ctx.send(f'You do not have the required role: {self.shutdown_role}')

    def help(self):
        return f"Shuts down the bot. Requires role `{self.shutdown_role}`."

async def setup(bot):
    await bot.add_cog(Shutdown(bot))