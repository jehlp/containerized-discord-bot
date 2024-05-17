from discord import File
from discord.ext import commands
from io import BytesIO
from src.cog import DiscordCog
from src.utils.general import file_is_too_large
from zipfile import ZipFile, ZIP_DEFLATED

class Compress(DiscordCog):
    @commands.command(name="compress")
    async def command(self, ctx):
        if not ctx.message.attachments:
            return
        try:
            attachment = ctx.message.attachments[0]
            data = BytesIO(await attachment.read())
            zbuffer = BytesIO()

            with ZipFile(zbuffer, "w", ZIP_DEFLATED) as z:
                z.writestr(attachment.filename, data.getvalue())

            if file_is_too_large(zbuffer):
                await ctx.send(f"Compressed file is too large to upload!")
            else:
                zbuffer.seek(0)
                zipped_file = File(fp=zbuffer, filename=f"{attachment.filename}.zip")
                await ctx.send(file=zipped_file)
        except Exception as e:
            await ctx.send(f"Unable to compress file: {e}")

async def setup(bot):
    await bot.add_cog(Compress(bot))