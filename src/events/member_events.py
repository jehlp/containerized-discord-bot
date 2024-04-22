import src.cog
from discord.ext import commands

class MemberEvents(src.cog.DiscordCog):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_event(f'{member} has joined the server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_event(f'{member} has left the server.')

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))