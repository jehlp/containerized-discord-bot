from asyncio import CancelledError, run
from discord.ext import commands
from src.utils.general import get_command_prefix, get_extensions, get_intents, get_token
from src.utils.asynchronous import graceful_shutdown, load_extensions

COMMAND_DIR = 'src/commands'
EVENT_DIR = 'src/events'

async def main():
    bot = commands.Bot(command_prefix=get_command_prefix(), intents=get_intents())
    try:
        async with bot:
            await load_extensions(bot, get_extensions(COMMAND_DIR))
            await load_extensions(bot, get_extensions(EVENT_DIR))
            await bot.start(get_token())
    except CancelledError:
        print("CancelledError caught (expected during shutdown)...")
    except Exception as e:
        print(f"An unexpected exception occurred: {e}")
    finally:
        if not bot.is_closed():
            await graceful_shutdown()
        print("Bot is closed. Cleanup done.")

if __name__ == '__main__':
    run(main())