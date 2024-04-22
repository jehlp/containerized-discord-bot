# Not part of stdlib
import discord 

class DiscordCog(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Disable the default help command
        self.bot.help_command = None

    async def log_event(self, message):
        print(message)

    def help(self):
        # If not overwritten, default 'help' is N/A
        return "No help available for this command."