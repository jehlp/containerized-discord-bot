import src.cog
from discord.ext import commands

class Prune(src.cog.DiscordCog):
    @commands.command(name='prune')
    async def command(self, ctx, num_to_delete=0):
        if num_to_delete:
            num_to_delete = min(num_to_delete, 100)
            await ctx.send(content=f'Pruning last {num_to_delete} messages...')
            await ctx.channel.purge(limit = num_to_delete + 1)

    def help(self):
        return "Removes the last specified number of messages in the channel. Usage: `!prune #`"

async def setup(bot):
    await bot.add_cog(Prune(bot))