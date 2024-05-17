from discord.ext import commands
from src.cog import DiscordCog
from src.utils.general import increment_user_xp

class MessageEvents(DiscordCog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.log_event(f'Message from {message.author}: {message.content}')

        # On message send, increase 'XP' of the sender
        increment_user_xp(message.author)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_event(f'A message by {message.author} was deleted: {message.content}')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.log_event(f'User {ctx.author} ran command: {ctx.command}')

async def setup(bot):
    await bot.add_cog(MessageEvents(bot))