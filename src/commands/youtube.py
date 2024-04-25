import asyncio
import discord
import os
import pytube
import src.cog
import threading
from discord.ext import commands

def download_file(stream, file_path, file_name):
    stream.download(output_path=file_path, filename=file_name, max_retries=10)

def on_progress(stream, chunk, bytes_remaining):
    print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

class YoutubeMP4(src.cog.DiscordCog):
    @commands.command(name='ytmp4')
    async def command(self, ctx, url=None, quality="720p"):
        format = "mp4"
        yt = None

        def send_file(stream, file_path):
            async def send_async():
                with open(file_path, 'rb') as file:
                    await ctx.send(file=discord.File(file))
            asyncio.run_coroutine_threadsafe(send_async(), ctx.bot.loop)

        try:
            yt = pytube.YouTube(url, on_progress_callback=on_progress, on_complete_callback=send_file)
        except pytube.exceptions.PytubeError:
            await ctx.send(content=f'Invalid URL!')
            return

        filter_streams = yt.streams.filter(file_extension=format, progressive=True)
        stream = filter_streams.get_by_resolution(quality)

        if not stream:
            await ctx.send(content='No matching stream of quality found, choosing lower quality one...')
            stream = filter_streams.get_lowest_resolution()

        file_name = f"temp_video.{format}"
        file_d = os.getcwd()
        file_path = os.path.join(os.getcwd(), file_name)

        if os.path.exists(file_path):
            os.remove(file_path)

        # Use another thread to avoid blocking further commands
        thread = threading.Thread(target=download_file, args=(stream, file_d, file_name))
        thread.start()

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: !ytmp4 <url> <quality>"

async def setup(bot):
    await bot.add_cog(YoutubeMP4(bot))