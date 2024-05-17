from asyncio import all_tasks, current_task
from os import getcwd
from os.path import exists, join
from shutil import rmtree
from src.utils.general import create_reaction_check

async def graceful_shutdown(bot):
    # Close external resources, in this case probably an aiohttp session
    if hasattr(bot, 'session') and not bot.session.closed:
        await bot.session.close()     
    tasks = [t for t in all_tasks() if t is not current_task()]
    for task in tasks:
        task.cancel()

    # Delete the ./tmp directory and all lingering resources within it (if they exist)
    tmp = join(getcwd(), "tmp")
    try:
        if exists(tmp):
            rmtree(tmp)
            print(f"Deleted the directory: {tmp}")
    except Exception as e:
        print(f"Failed to delete {tmp}: {e}")

    await bot.close()

async def load_extensions(bot, extensions):
    for extension in extensions:
        await bot.load_extension(extension)
        print("loaded", extension)

async def navigate(bot, ctx, message, emojis, items, update_func, timeout=60.0):
    current_index = 0
    user = ctx.author
    message_id = message.id

    while True:
        try:
            reaction, _ = await bot.wait_for(
                'reaction_add',
                timeout=timeout,
                check=create_reaction_check(message_id, user, emojis)
            )
            if str(reaction.emoji) == '➡️' and current_index < len(items) - 1:
                current_index += 1
            elif str(reaction.emoji) == '⬅️' and current_index > 0:
                current_index -= 1
            elif str(reaction.emoji) == '⬇️': 
                return current_index, 'download'

            await update_func(current_index, items)
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            break
    return current_index, 'timeout'