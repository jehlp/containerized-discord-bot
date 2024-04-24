import src.cog
import src.utils.general
import src.utils.asynchronous
from discord.ext import commands

class Shutdown(src.cog.DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.shutdown_role = src.utils.general.get_shutdown_role()

    @commands.command(name='shutdown')
    async def command(self, ctx):
        if src.utils.general.has_role(ctx.author, self.shutdown_role):
            await ctx.send('Shutting down... 👋')
            await src.utils.asynchronous.graceful_shutdown(self.bot)
        else:
            await ctx.send(f'You do not have the required role: {self.shutdown_role}')

    def help(self):
        return f"Shuts down the bot. Requires role `{self.shutdown_role}`."

async def setup(bot):
    await bot.add_cog(Shutdown(bot))