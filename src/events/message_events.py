# Not part of stdlib
from discord.ext import commands

# Internal
from ._master_event import DiscordEvent

class MessageEvents(DiscordEvent):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await self.log_event(f'Message from {message.author}: {message.content}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_event(f'A message by {message.author} was deleted: {message.content}')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        await self.log_event(f'User {ctx.author} ran command: {ctx.command}')

async def setup(bot):
    await bot.add_cog(MessageEvents(bot))