import asyncio
import src.utils
from discord.ext import commands

COMMAND_DIR = 'src/commands'
EVENT_DIR = 'src/events'

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)
        print("loaded", extension)

async def main():
    bot = commands.Bot(command_prefix=src.utils.get_command_prefix(), intents=src.utils.get_intents())
    try:
        async with bot:
            await load_extensions(bot, src.utils.get_extensions(COMMAND_DIR))
            await load_extensions(bot, src.utils.get_extensions(EVENT_DIR))
            await bot.start(src.utils.get_token())
    except asyncio.CancelledError:
        print("CancelledError caught (expected during shutdown)...")
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
    finally:
        if not bot.is_closed():
            await bot.close()
        print("Bot is closed. Cleanup done.")

if __name__ == '__main__':
    asyncio.run(main())