import configparser
import os

# Not part of stdlib
import discord

def get_intents():
    config = configparser.ConfigParser()
    config.read('./conf/config.ini')

    intents = discord.Intents.default()
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

def get_extensions():
    extensions = []
    for filename in os.listdir('src/commands'):
        if filename.endswith('.py') and not filename.startswith('_'):
            # Removes the '.py' from the filename
            extension_name = f"commands.{filename[:-3]}" 
            extensions.append(extension_name)
    return extensions
