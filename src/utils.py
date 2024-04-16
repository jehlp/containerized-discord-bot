import configparser
import os

# Not part of stdlib
import discord

BASE_DIR = 'src'
CONFIG_PATH = './conf/config.ini'

def get_command_prefix():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    # Default command prefix is '!'
    return config.get('settings', 'command_prefix', fallback='!')

def get_extensions(directory):
    extensions = []
    subdirectory_path = os.path.basename(directory)
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('_'):
            # Removes the '.py' from the filename
            extension_name = f"{BASE_DIR}.{subdirectory_path}.{filename[:-3]}" 
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