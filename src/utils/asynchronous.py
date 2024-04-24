import asyncio

async def graceful_shutdown(bot):
    # Close external resources, in this case probably an aiohttp session
    if hasattr(bot, 'session') and not bot.session.closed:
        await bot.session.close()     
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await bot.close()

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)
        print("loaded", extension)