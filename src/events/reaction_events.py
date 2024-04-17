# Not part of stdlib
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class ReactionEvents(DiscordCog):
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.log_event(f'{user} added {reaction.emoji} to {reaction.message.content}')

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.log_event(f'{user} removed their {reaction.emoji} from {reaction.message.content}')

async def setup(bot):
    await bot.add_cog(ReactionEvents(bot))
