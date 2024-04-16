# Not part of stdlib
from discord.ext import commands

# Internal
from ..cog import DiscordCog

class GuildEvents(DiscordCog):
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        await self.log_event(f'Guild updated from {before.name} to {after.name}')

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.log_event(f'Role created: {role.name}') 

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.log_event(f'Role deleted: {role.name}')

async def setup(bot):
    await bot.add_cog(GuildEvents(bot))
