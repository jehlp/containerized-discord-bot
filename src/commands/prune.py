# Not part of stdlib
from discord.ext import commands

# Internal
from src.cog import DiscordCog

class Prune(DiscordCog):
    @commands.command(name='prune')
    async def command(self, ctx, num_to_delete: int = 0):
        num_to_delete = min(num_to_delete, 100)
        await ctx.send(content=f'Pruning last {num_to_delete} messages...')
        await ctx.channel.purge(limit = num_to_delete + 2) # include issued command and bot response

    def help(self):
        return "Removes the last specified number of messages in the channel. Requires manage message and read message history permissions in the channel. Usage: !prune #"

async def setup(bot):
    await bot.add_cog(Prune(bot))