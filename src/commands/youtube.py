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

class YoutubeDL(DiscordCog):
    @commands.command(name='yt')
    async def command(self, ctx, url: str = None, format: str = "mp4", quality: str = "720p"):
        if format != "mp4" and format != "mp3":
            await ctx.send(content=f'Invalid file format! Expected: mp3|mp4')
            return

        yt = None

        try:
            yt = YouTube(url, on_progress_callback=on_progress, allow_oauth_cache=True)
        except PytubeError:
            await ctx.send(content=f'Invalid URL!')
            return

        print("Youtube Object retrieved")

        match format:
            case "mp4":
                stream = yt.streams.get_by_resolution(quality)
            case "mp3":
                stream = yt.streams.get_audio_only()

        if not stream:
            print("Could not retrieve stream")
            return

        file_name = "yt_download." + format
        file_dir = os.getcwd()
        file_path = os.path.join(file_dir, file_name)
        print(file_path)

        # remove temp yt_download file
        if os.path.exists(file_path):
            os.remove(file_path)

        print("Starting download")
        await download_file(stream, file_dir, file_name, ctx)

    def help(self):
        return "Takes a youtube url and returns a file of specified type (mp3|mp4). Defaults to mp4. Usage: !yt <url> <type>"

async def setup(bot):
    await bot.add_cog(YoutubeDL(bot))