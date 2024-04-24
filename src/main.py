import asyncio
import src.utils.general
import src.utils.asynchronous
from discord.ext import commands

COMMAND_DIR = 'src/commands'
EVENT_DIR = 'src/events'

async def main():
    bot = commands.Bot(command_prefix=src.utils.general.get_command_prefix(), intents=src.utils.general.get_intents())
    try:
        async with bot:
            await src.utils.asynchronous.load_extensions(bot, src.utils.general.get_extensions(COMMAND_DIR))
            await src.utils.asynchronous.load_extensions(bot, src.utils.general.get_extensions(EVENT_DIR))
            await bot.start(src.utils.general.get_token())
    except asyncio.CancelledError:
        print("CancelledError caught (expected during shutdown)...")
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
    finally:
        if not bot.is_closed():
            await src.utils.asynchronous.graceful_shutdown()
        print("Bot is closed. Cleanup done.")

if __name__ == '__main__':
    asyncio.run(main())