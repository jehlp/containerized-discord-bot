import asyncio

# Not part of stdlib
from discord.ext import commands

# Internal
import utils

async def main():
    intents = utils.load_intents()
    token = utils.load_token()

    bot = commands.Bot(command_prefix='!', intents=intents)
    await bot.load_extension('commands')
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())