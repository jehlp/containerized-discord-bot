import asyncio
import bs4
import discord
import requests
import src.cog
import src.utils.general
import urllib.parse
from discord.ext import commands

class ImageSearch(src.cog.DiscordCog):
    @commands.command(name='img')
    async def command(self, ctx, *, search_term=None):
        if not search_term:
            return

        images = self.scrape_images_from_google(search_term)
        current_index = 0
        total_images = len(images)

        footer_text = f"Image {current_index + 1} of {total_images} | Search results for '{search_term}'"
        message = await ctx.send(embed=src.utils.general.create_image_embed(images[0], footer_text))

        for emoji in ['⬅️', '➡️']:
            await message.add_reaction(emoji)

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    'reaction_add', 
                    timeout=60.0, 
                    check=lambda reaction, user: str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == message.id
                )
                if str(reaction.emoji) == '➡️':
                    current_index = (current_index + 1) % len(images)
                elif str(reaction.emoji) == '⬅️':
                    current_index = (current_index - 1) % len(images)

                footer_text = f"Image {current_index + 1} of {total_images} | Search results for '{search_term}'"
                await message.edit(embed=src.utils.general.create_image_embed(images[current_index], footer_text))
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break

    def scrape_images_from_google(self, search_term):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(f"https://www.google.com/search?hl=en&tbm=isch&q={urllib.parse.quote(search_term)}", headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # Don't return the first result from the webscraper, it's usually the google logo
        return [img['src'] for img in soup.find_all('img')][1:] 

    def help(self):
        return "Scrapes the web for images matching a search term. Usage: `!img <search-term>`"

async def setup(bot):
    await bot.add_cog(ImageSearch(bot))
