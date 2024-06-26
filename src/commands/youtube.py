from asyncio import sleep
from conf.constants import BYTES_PER_KB
from discord import Color, File
from discord.ext import commands
from os import getcwd, makedirs, remove, rename
from os.path import join
from pytube import Search, YouTube
from src.cog import DiscordCog
from src.utils.asynchronous import navigate
from src.utils.general import create_embed, file_is_too_large, get_max_upload_size_mb
from subprocess import run
from threading import Event, Thread
from uuid import uuid4

class YoutubeSearch(DiscordCog):
    @commands.command(name='yt')
    async def command(self, ctx, *, search_term=None):
        search = Search(search_term)
        results = list(search.results)

        if not results:
            await ctx.send("No results found.")
            return
            
        current_index = 0
        embed = create_embed(
            title=f'{results[current_index].title}',
            url=f"https://www.youtube.com/watch?v={results[current_index].video_id}",
            color=Color.red(),
            thumbnail=results[current_index].thumbnail_url,
            footer_text=f"Video {current_index + 1} of {len(results)} | Search results for `{search_term}`"
        )
        message = await ctx.send(embed=embed)

        emojis = ['⬅️', '➡️', '⬇️']
        for emoji in emojis:
            await message.add_reaction(emoji)

        async def update_func(index, items):
            new_embed = create_embed(
                title=f'{items[index].title}',
                url=f"https://www.youtube.com/watch?v={items[index].video_id}",
                color=Color.red(),
                thumbnail=items[index].thumbnail_url,
                footer_text=f"Video {index + 1} of {len(items)} | Search results for `{search_term}`"
            )
            await message.edit(embed=new_embed)

        index, action = await navigate(self.bot, ctx, message, emojis, results, update_func)
        if action == 'download':
            video_url = f"https://www.youtube.com/watch?v={results[index].video_id}"
            await ctx.invoke(self.bot.get_command('ytmp4'), url=video_url)
            await message.clear_reactions()
        
    def help(self):
        return "Browses youtube for a search term. Down arrow reacting on a result will download the video. Usage: `!yt <search-term>`"

class YoutubeToMP4(DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.format = 'mp4'
        self.progress_message = None
        self.total_bytes = 0
        self.upload_ready = False
        self.yt_title = ""
        self.yt_author = ""

    def download_file(self, stream, file_path, file_name, completion_event):
        self.total_bytes = stream.filesize
        stream.download(output_path=file_path, filename=file_name)
        completion_event.set()

    def on_progress(self, stream, chunk, bytes_remaining):
        print(f"Fetching {stream} --> Bytes remaining: {bytes_remaining}")

        progress = (self.total_bytes - bytes_remaining) / self.total_bytes

        # Because of Discord API rate limits, we only update the progress bar at intervals of 5%
        if int(100 * progress) % 5 == 0 or bytes_remaining == 0:
            embed = create_embed(
                title="Downloading...",
                description=f"{self.yt_title} by {self.yt_author}\nProgress: {'█' * int(20 * progress) + '░' * int(20 * (1 - progress))} {int(100 * progress)}%",
                color=Color.gold()
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

    def trim_file(self, file_path):
        temp_file_path = f"{file_path}.temp"
        ffmpeg_command = [
            "ffmpeg", "-i", file_path, "-fs", str(int(get_max_upload_size_mb() * (BYTES_PER_KB ** 2))), 
            "-c", "copy", "-f", self.format, temp_file_path
        ]
        print("Executing:", ' '.join(ffmpeg_command))        
        result = run(ffmpeg_command, capture_output=True)
        if result.returncode != 0:
            print("ffmpeg failed:", result.stderr)

        # Replace the original file with the trimmed one
        remove(file_path)
        rename(temp_file_path, file_path)

    @commands.command(name='ytmp4')
    async def command(self, ctx, url=None, quality="720p"):
        if not url:
            await ctx.send(content="Please provide a URL!")
            return

        tmp = join(getcwd(), "tmp")
        makedirs(tmp, exist_ok=True)

        file_name = f"temp_video_{uuid4()}.{self.format}"
        file_path = join(tmp, file_name)

        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            self.yt_title = yt.title
            self.yt_author = yt.author
            filter_streams = yt.streams.filter(file_extension=self.format, progressive=True)
            stream = filter_streams.get_by_resolution(quality)
            if not stream:
                stream = filter_streams.get_lowest_resolution()

            initial_embed = create_embed(
                title="Initializing Download...",
                description=f"{self.yt_title} by {self.yt_author}", 
                color=Color.gold()
            )
            self.progress_message = await ctx.send(embed=initial_embed)

            # Download the file in its own thread
            download_complete = Event()
            download_thread = Thread(target=self.download_file, args=(stream, tmp, file_name, download_complete))
            download_thread.start()
            download_complete.wait()

            # Block the rest of the code until the progress bar has finished updating
            while not self.upload_ready:
                await sleep(0.5)

            if file_is_too_large(file_path):
                self.trim_file(file_path)
            with open(file_path, 'rb') as file:
                await ctx.send(file=File(file))  

            final_embed = create_embed(
                title="Download Complete!",
                description=f"{self.yt_title} by {self.yt_author}", 
                color=Color.green()
            )
            await self.progress_message.edit(embed=final_embed)

            # Clean up the local video file when done
            remove(file_path)
        except Exception as e:
            await ctx.send(content=f'Failed to download video: {e}')

    def help(self):
        return "Takes a youtube url and returns a mp4 of specified quality (720p default). Usage: `!ytmp4 <url> <quality>`"

async def setup(bot):
    await bot.add_cog(YoutubeToMP4(bot))
    await bot.add_cog(YoutubeSearch(bot))