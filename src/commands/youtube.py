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

def download_file(stream, file_path, file_name, completion_event):
    stream.download(output_path=file_path, filename=file_name)
    completion_event.set()

def trim_file_if_too_large(file_path, format='mp4'):
    max_file_size_mb = src.utils.general.get_max_upload_size_mb() * 0.9 # Give some breathing room
    file_size_mb = os.path.getsize(file_path) / (BYTES_PER_KB ** 2)
    if file_size_mb > max_file_size_mb:
        # Trim the video to the maximum file size
        temp_file_path = f"{file_path}.temp"
        ffmpeg_command = [
            "ffmpeg", "-i", file_path, "-fs", str(int(max_file_size_mb * (BYTES_PER_KB ** 2))), 
            "-c", "copy", "-f", format, temp_file_path
        ]
        print("Executing:", ' '.join(ffmpeg_command))        
        result = subprocess.run(ffmpeg_command, capture_output=True)
        if result.returncode != 0:
            print("ffmpeg failed:", result.stderr)
            return False
        os.remove(file_path)
        os.rename(temp_file_path, file_path)
    return True

def on_progress(stream, chunk, bytes_remaining):
    print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

class YoutubeToMP4(src.cog.DiscordCog):
    @commands.command(name='ytmp4')
    async def command(self, ctx, url=None, quality="720p"):
        if not url:
            await ctx.send(content="Please provide a URL!")
            return

        format = "mp4"
        file_name = f"temp_video_{uuid.uuid4()}.{format}"
        file_path = os.path.join(os.getcwd(), file_name)

        try:
            yt = pytube.YouTube(url, on_progress_callback=on_progress)
            filter_streams = yt.streams.filter(file_extension=format, progressive=True)
            stream = filter_streams.get_by_resolution(quality)
            if not stream:
                stream = filter_streams.get_lowest_resolution()

            download_complete = threading.Event()
            download_thread = threading.Thread(target=download_file, args=(stream, os.getcwd(), file_name, download_complete))
            download_thread.start()
            download_complete.wait() # Wait here until the download is signaled to be complete

            if trim_file_if_too_large(file_path, format):
                try:
                    with open(file_path, 'rb') as file:
                        await ctx.send(file=discord.File(file))
                finally:
                    os.remove(file_path)
        except Exception as e:
            await ctx.send(content=f'Failed to download video: {e}')

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: `!ytmp4 <url> <quality>`"

async def setup(bot):
    await bot.add_cog(YoutubeToMP4(bot))