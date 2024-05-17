from conf.constants import BYTES_PER_KB
from configparser import ConfigParser
from discord import Color, Embed, Intents
from discord.ext import commands
from discord.utils import get
from io import BytesIO
from os import getenv, walk, sep
from os.path import getsize, relpath
from src.utils.postgres import get_user_xp, update_user_xp

BASE_DIR = 'src'
CONFIG_PATH = './conf/config.ini'

def create_embed(title=None, description=None, url=None, image_url=None, footer_text=None, thumbnail=None, color=Color.teal()):
    embed = Embed(color=color)
    if title:
        embed.title = title
    if description:
        embed.description = description
    if url:
        embed.url = url
    if image_url:
        embed.set_image(url=image_url)
    if footer_text:
        embed.set_footer(text=footer_text)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed

def create_reaction_check(message_id, user, emojis):
    def check(reaction, reactor):
        return (
            reactor == user and
            reaction.message.id == message_id and
            str(reaction.emoji) in emojis
        )
    return check

def file_is_too_large(file_path_or_bytesio_obj):
    # Function may accept either a file_path or a BytesIO file object
    try:
        if isinstance(file_path_or_bytesio_obj, BytesIO):
            file_size_mb = len(file_path_or_bytesio_obj.getvalue()) / (BYTES_PER_KB ** 2)
        else:
            file_size_mb = getsize(file_path_or_bytesio_obj) / (BYTES_PER_KB ** 2)
        return file_size_mb > get_max_upload_size_mb()
    except Exception as e:
        print(f"Unable to determine if file of type {type(file_path_or_bytesio_obj)} is too large to upload: {e}")

def get_command_prefix():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    # Default command prefix is '!'
    return config.get('settings', 'command_prefix', fallback='!')

def get_extensions(directory):
    extensions = []
    for dirpath, dirnames, filenames in walk(directory):
        # In an extension dir, all .py files not starting with '_' are treated as extensions
        py_files = [f for f in filenames if f.endswith('.py') and not f.startswith('_')]
        for filename in py_files:
            rel_path = relpath(dirpath, BASE_DIR)
            module_path = rel_path.replace(sep, '.')
            # The [:-3] is just to remove the '.py' extension (because we're loading a module)
            extension_name = f"{BASE_DIR}.{module_path}.{filename[:-3]}"
            extensions.append(extension_name)
    return extensions

def get_intents():
    config = ConfigParser()
    config.read(CONFIG_PATH)

    intents = Intents.default()

    # All intents are set in /conf/config.ini:
    # intents.guilds controls if bot can access guilds (servers) data
    # intents.members controls if bot can track changes of members in a guild (e.g., role changes, joins, leaves)
    # intents.presences controls if bot can access presence information (e.g., whether a user is online, what game they're playing)
    # intents.messages controls if bot can receive messages in channels
    # intents.message_content controls if bot can read message content itself

    intents.guilds = config.getboolean('intents', 'guilds')
    intents.members = config.getboolean('intents', 'members')
    intents.presences = config.getboolean('intents', 'presences')
    intents.messages = config.getboolean('intents', 'messages')
    intents.message_content = config.getboolean('intents', 'message_content')

    return intents

def get_max_upload_size_mb():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    # Default upload size is 16MB (Non-Nitro)
    return int(config.get('settings', 'max_upload_size_mb', fallback=16)) * 0.9 # Give some breathing room

def get_shutdown_role():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    # Default shutdown role is 'administrator'
    return config.get('settings', 'shutdown_role', fallback='administrator')

def get_token():
    try:
        return getenv('DISCORD_TOKEN').strip()
    except AttributeError:
        print("Error: DISCORD_TOKEN environment variable not set.")
        exit()

def has_role(author, role_name):
    role = get(author.guild.roles, name=role_name)
    return role in author.roles

def increment_user_xp(author, dx=10):
    try:
        xp = get_user_xp(author.id) or 0
        update_user_xp(author.id, dx)
        print(f"User {author}'s XP updated from {xp} to {xp + dx}")
    except Exception as e:
        print(f"Failed to update XP for {author}: {e}")

def split_camel_case(my_str):
    new_str = []
    for idx in range(len(my_str)):
        if idx > 1 and my_str[idx].isupper() and my_str[idx - 1].islower():
            new_str.append(" ")
        new_str.append(my_str[idx])
    return "".join(new_str)