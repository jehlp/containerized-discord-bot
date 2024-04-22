import src.cog
from discord.ext import commands

class ReactionEvents(src.cog.DiscordCog):
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.log_event(f'{user} added {reaction.emoji} to {reaction.message.content}')

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.log_event(f'{user} removed their {reaction.emoji} from {reaction.message.content}')

async def setup(bot):
    await bot.add_cog(ReactionEvents(bot))
