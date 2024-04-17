import configparser
import os

# Not part of stdlib
import discord

# Internal
import src.postgres as postgres

BASE_DIR = 'src'
CONFIG_PATH = './conf/config.ini'

def get_command_prefix():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    # Default command prefix is '!'
    return config.get('settings', 'command_prefix', fallback='!')

def get_extensions(directory):
    extensions = []
    for dirpath, dirnames, filenames in os.walk(directory):
        # In an extension dir, all .py files not starting with '_' are treated as extensions
        py_files = [f for f in filenames if f.endswith('.py') and not f.startswith('_')]
        for filename in py_files:
            rel_path = os.path.relpath(dirpath, BASE_DIR)
            module_path = rel_path.replace(os.sep, '.')
            # The [:-3] is just to remove the '.py' extension (because we're loading a module)
            extension_name = f"{BASE_DIR}.{module_path}.{filename[:-3]}"
            extensions.append(extension_name)
    return extensions

def get_intents():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    intents = discord.Intents.default()

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

def get_token():
    try:
        return os.getenv('DISCORD_TOKEN').strip()
    except AttributeError:
        print("Error: DISCORD_TOKEN environment variable not set.")
        exit()

def increment_user_xp(author, dx=10):
    try:
        xp = postgres.get_user_xp(author.id) or 0
        postgres.update_user_xp(author.id, dx)
        print(f"User {author}'s XP updated from {xp} to {xp + dx}")
    except Exception as e:
        print(f"Failed to update XP for {author}: {e}")

