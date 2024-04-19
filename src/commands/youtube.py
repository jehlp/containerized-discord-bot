import os
from threading import Thread

# Not part of stdlib
from pytube import YouTube
from pytube.exceptions import PytubeError
import discord
from discord.ext import commands

# Internal
from src.cog import DiscordCog

def download_file(stream, file_path, file_name):
    stream.download(output_path=file_path, filename=file_name, max_retries=10)

def on_progress(stream, chunk, bytes_remaining):
    print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

class YoutubeMP4(DiscordCog):
    @commands.command(name='ytmp4')
    async def command(self, ctx, url: str = None, quality: str = "720p"):
        format = "mp4"
        yt = None

        def send_file(stream, file_path):
            with open(file_path, 'rb') as file:
                ctx.send(file=discord.File(file), timeout=90, max_retries=10)

        try:
            yt = YouTube(url, on_progress_callback=on_progress, on_complete_callback=send_file)
        except PytubeError:
            await ctx.send(content=f'Invalid URL!')
            return

        # progressive mode must be true
        filter_streams = yt.streams.filter(file_extension=format, progressive=True)
        stream = filter_streams.get_by_resolution(quality)

        if not stream:
            await ctx.send(content='No matching stream of quality found, choosing lower quality one...')
            stream = filter_streams.get_lowest_resolution()

        file_name = "temp_video."+format
        file_d = os.getcwd()
        file_path = os.path.join(file_d, file_name)

        # remove temp_video if it exists 
        if os.path.exists(file_path):
            os.remove(file_path)

        # use another thread to avoid blocking further commands
        thread = Thread(target=download_file, args = (stream, file_d, file_name))
        thread.start()

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: !ytmp4 <url> <quality>"

async def setup(bot):
    await bot.add_cog(YoutubeMP4(bot))