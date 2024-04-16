import asyncio

# Not part of stdlib
from discord.ext import commands

# Internal
import utils

COMMAND_DIR = 'src/commands'
EVENT_DIR = 'src/events'

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)
        print("loaded", extension)

async def main():
    bot = commands.Bot(command_prefix=utils.get_command_prefix(), intents=utils.get_intents())
    async with bot:
        await load_extensions(bot, utils.get_extensions(COMMAND_DIR))
        await load_extensions(bot, utils.get_extensions(EVENT_DIR))
        await bot.start(utils.get_token())

if __name__ == '__main__':
    asyncio.run(main())