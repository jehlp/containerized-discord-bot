# Not part of stdlib
from discord.ext import commands

# Internal
import src.utils as utils
from ..cog import DiscordCog

class MessageEvents(DiscordCog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # On message send, increase 'XP' of the sender
        utils.increment_user_xp(message.author)
        
        await self.log_event(f'Message from {message.author}: {message.content}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_event(f'A message by {message.author} was deleted: {message.content}')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.log_event(f'User {ctx.author} ran command: {ctx.command}')

async def setup(bot):
    await bot.add_cog(MessageEvents(bot))