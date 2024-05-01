import discord
import io
import src.cog
import src.utils.general
import zipfile
from discord.ext import commands

class Compress(src.cog.DiscordCog):
	@commands.command(name='compress')
	async def command(self, ctx):
		if not ctx.message.attachments:
			return

		try:
			attachment = ctx.message.attachments[0]
			data = io.BytesIO(await attachment.read())
			zbuffer = io.BytesIO()

			with zipfile.ZipFile(zbuffer, 'w', zipfile.ZIP_DEFLATED) as z:
				z.writestr(attachment.filename, data.getvalue())

			if src.utils.general.file_is_too_large(zbuffer):
				await ctx.send(f"Compressed file is too large to upload!")
			else:	
				zbuffer.seek(0)
				zipped_file = discord.File(fp=zbuffer, filename=f'{attachment.filename}.zip')
				await ctx.send(file=zipped_file)
		except Exception as e:
			await ctx.send(f"Unable to compress file: {e}")

async def setup(bot):
	await bot.add_cog(Compress(bot))