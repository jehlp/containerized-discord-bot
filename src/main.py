import asyncio

# Not part of stdlib
from discord.ext import commands

# Internal
import utils

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)

async def main():
    bot = commands.Bot(command_prefix='!', intents=utils.get_intents())
    async with bot:
        await load_extensions(bot, utils.get_extensions())
        await bot.start(utils.get_token())

if __name__ == '__main__':
    asyncio.run(main())