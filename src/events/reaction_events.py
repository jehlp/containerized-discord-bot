# Not part of stdlib
from discord.ext import commands

# Internal
from ._master_event import DiscordEvent

class ReactionEvents(DiscordEvent):
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.log_event(f'{user} added {reaction.emoji} to {reaction.message.content}')

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.log_event(f'{user} removed their {reaction.emoji} from {reaction.message.content}')

async def setup(bot):
    await bot.add_cog(ReactionEvents(bot))
