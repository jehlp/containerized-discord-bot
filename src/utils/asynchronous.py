import asyncio
import shutil
import os

async def graceful_shutdown(bot):
    # Close external resources, in this case probably an aiohttp session
    if hasattr(bot, 'session') and not bot.session.closed:
        await bot.session.close()     
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    # Delete the ./tmp directory and all lingering resources within it (if they exist)
    tmp = os.path.join(os.getcwd(), "tmp")
    try:
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
            print(f"Deleted the directory: {tmp}")
    except Exception as e:
        print(f"Failed to delete {tmp}: {e}")

    await bot.close()

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)
        print("loaded", extension)