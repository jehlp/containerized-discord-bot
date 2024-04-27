import bs4
import discord
import nltk
import random
import requests
import src.cog
import src.utils.asynchronous
import src.utils.general
import urllib
from discord.ext import commands

def scrape_images_from_google(search_term):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/58.0.3029.110 Safari/537.3"}
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={urllib.parse.quote(search_term)}"
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # Don't return the first result from the webscraper, it's usually the google logo
    return [img['src'] for img in soup.find_all('img')][1:] 

class ImageSearch(src.cog.DiscordCog):
    def __init__(self, bot):
        super().__init__(bot)
        # Download the corpus on initialization instead of runtime
        nltk.download('brown')
        words = nltk.corpus.brown.words()
        self.word_list = [word for word, count in nltk.probability.FreqDist(words).most_common(5000) if len(word) <= 8]

    @commands.command(name='img')
    async def command(self, ctx, *, search_term=None):
        if not search_term:
            search_term = ' '.join(random.sample(self.word_list, 2))

        images = scrape_images_from_google(search_term)
        current_index = 0
        total_images = len(images)

        footer_text = f"Image {current_index + 1} of {total_images} | Search results for '{search_term}'"
        inital_embed = src.utils.general.create_embed(
            image_url=images[0], 
            footer_text=footer_text
        )
        message = await ctx.send(embed=inital_embed)

        emojis = ['⬅️', '➡️']

        for emoji in emojis:
            await message.add_reaction(emoji)

        async def update_func(index, items):
            new_embed = src.utils.general.create_embed(
                image_url=items[index], 
                footer_text=f"Image {index + 1} of {len(items)} | Search results for '{search_term}'"
            )
            await message.edit(embed=new_embed)

        await src.utils.asynchronous.navigate(self.bot, ctx, message, emojis, images, update_func)

    def help(self):
        return "Scrapes the web for images matching a search term. If no search term is provided, it will be generated at random. Usage: `!img <search-term>`"

async def setup(bot):
    await bot.add_cog(ImageSearch(bot))