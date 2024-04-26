import asyncio
import discord
import os
import pytube
import src.cog
import src.utils.general
import subprocess
import threading
import uuid
from discord.ext import commands

BYTES_PER_KB = 1024

class YoutubeToMP4(src.cog.DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.progress_message = None
        self.total_bytes = 0
        self.yt_title = ""
        self.yt_author = ""
        self.upload_ready = False
        self.max_file_size_mb = src.utils.general.get_max_upload_size_mb() * 0.9 # Give some breathing room

    def download_file(self, stream, file_path, file_name, completion_event):
        self.total_bytes = stream.filesize
        stream.download(output_path=file_path, filename=file_name)
        completion_event.set()

    def file_is_too_large(self, file_path):
        file_size_mb = os.path.getsize(file_path) / (BYTES_PER_KB ** 2)
        return file_size_mb > self.max_file_size_mb

    def on_progress(self, stream, chunk, bytes_remaining):
        print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

        progress = (self.total_bytes - bytes_remaining) / self.total_bytes

        # Because of Discord rate limits, we only update the progress bar at intervals of 5%
        if int(100 * progress) % 5 == 0 or bytes_remaining == 0:
            embed = discord.Embed(
                title="Downloading...",
                description=f"{self.yt_title} by {self.yt_author}\nProgress: {'█' * int(20 * progress) + '░' * int(20 * (1 - progress))} {int(100 * progress)}%",
                color=discord.Color.gold()
            )
            # Note that also because of rate limits, the bar is updated when the event loop processes
            # the requests, and not actually when the chunks are downloaded in real time.
            task = self.bot.loop.create_task(self.progress_message.edit(embed=embed))
            task.add_done_callback(self.on_update_complete)

    # Callback for the progress bar
    def on_update_complete(self, task):
        result = task.result()
        if result.embeds[0].description[-4:] == '100%':
            self.upload_ready = True

    def trim_file(self, file_path, format):
        temp_file_path = f"{file_path}.temp"
        ffmpeg_command = [
            "ffmpeg", "-i", file_path, "-fs", str(int(self.max_file_size_mb * (BYTES_PER_KB ** 2))), 
            "-c", "copy", "-f", format, temp_file_path
        ]
        print("Executing:", ' '.join(ffmpeg_command))        
        result = subprocess.run(ffmpeg_command, capture_output=True)
        if result.returncode != 0:
            print("ffmpeg failed:", result.stderr)
        os.remove(file_path)
        os.rename(temp_file_path, file_path)

    @commands.command(name='ytmp4')
    async def command(self, ctx, url=None, quality="720p"):
        if not url:
            await ctx.send(content="Please provide a URL!")
            return

        format = "mp4" # TODO: support other video formats?

        tmp = os.path.join(os.getcwd(), "tmp")
        os.makedirs(tmp, exist_ok=True)

        file_name = f"temp_video_{uuid.uuid4()}.{format}"
        file_path = os.path.join(tmp, file_name)

        try:
            yt = pytube.YouTube(url, on_progress_callback=self.on_progress)
            self.yt_title = yt.title
            self.yt_author = yt.author
            filter_streams = yt.streams.filter(file_extension=format, progressive=True)
            stream = filter_streams.get_by_resolution(quality)
            if not stream:
                stream = filter_streams.get_lowest_resolution()

            initial_embed = discord.Embed(
                title="Initializing Download...",
                description=f"{self.yt_title} by {self.yt_author}", 
                color=discord.Color.gold()
            )

            self.progress_message = await ctx.send(embed=initial_embed)

            # Download the file in its own thread
            download_complete = threading.Event()
            download_thread = threading.Thread(target=self.download_file, args=(stream, tmp, file_name, download_complete))
            download_thread.start()
            download_complete.wait()

            # Block the rest of the code until the progress bar has finished updating
            while not self.upload_ready:
                await asyncio.sleep(0.5)

            try:
                if self.file_is_too_large(file_path):
                    self.trim_file(file_path, format)
                with open(file_path, 'rb') as file:
                    await ctx.send(file=discord.File(file))              
                final_embed = discord.Embed(
                    title="Download Complete!",
                    description=f"{self.yt_title} by {self.yt_author}", 
                    color=discord.Color.green()
                )
                await self.progress_message.edit(embed=final_embed)
            finally:
                os.remove(file_path)
        except Exception as e:
            await ctx.send(content=f'Failed to download video: {e}')

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: `!ytmp4 <url> <quality>`"

async def setup(bot):
    await bot.add_cog(YoutubeToMP4(bot))