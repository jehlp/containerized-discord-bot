import os

# Not part of stdlib
from pytube import YouTube
from pytube.exceptions import PytubeError
import discord
from discord.ext import commands

# Internal
from src.cog import DiscordCog

async def send_file(file, ctx):
    with open(file, 'rb') as file:
        await ctx.send(file=discord.File(file))

async def download_file(stream, file_d, file_name, ctx):
    file = stream.download(output_path=file_d, filename=file_name, max_retries=10)
    await send_file(file, ctx)

def on_progress(stream, chunk, bytes_remaining):
    print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

class YoutubeMP4(DiscordCog):
    @commands.command(name='ytmp4')
    async def command(self, ctx, url: str = None, quality: str = "720p"):
        format = "mp4"
        yt = None

        try:
            yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True)
        except PytubeError:
            await ctx.send(content=f'Invalid URL!')
            return

        print("Youtube Object retrieved")
        stream = yt.streams.get_by_resolution(quality)

        if not stream:
            await ctx.send(content='No matching stream of quality found, choosing lower quality one...')
            stream = yt.streams.get_lowest_resolution()

        file_name = "temp_video."+format
        file_dir = os.getcwd()
        file_path = os.path.join(file_dir, file_name)

        # remove temp_video if it exists 
        if os.path.exists(file_path):
            os.remove(file_path)

        print("Starting download")
        await download_file(stream, file_dir, file_name, ctx)

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: !ytmp4 <url> <quality>"

async def setup(bot):
    await bot.add_cog(YoutubeMP4(bot))