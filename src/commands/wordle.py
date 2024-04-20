from collections import defaultdict

# Not part of stdlib
from discord.ext import commands

# Internal
from src.cog import DiscordCog
import src.utils as utils

class WordleGame:
    GAMES = {}
    NUM_GUESSES = 5 # number of guess attempts

    @staticmethod
    def get(channel) -> 'WordleGame':
        return WordleGame.GAMES.get(channel)

    def __init__(self, length, channel):
        # try to get valid word of length
        word = utils.get_random_word(length)

        if not word:
            raise ValueError("Failed to find a valid word of specified length.")

        self.channel = channel
        self.attempts = self.NUM_GUESSES
        self.word = word
        self.length = length
        self.hint = ['_'] * length

        # add instance to games list
        self.GAMES[channel] = self

    def guess(self, guess: str) -> str:
        # make sure guess is same length and contains only alphabetical characters
        if self.length != len(guess) or not guess.isalpha():
            return 'Invalid guess! Try again.'
        else:
            success = True
            letter_count = defaultdict(int)
            guess = guess.lower()

            # map letter count
            for letter in self.word:
                letter_count[letter] += 1

            # update guess hint
            for i in range(self.length):
                if self.word[i] == guess[i]:
                    self.hint[i] = guess[i]
                elif guess[i] in self.word and letter_count[guess[i]] > 0:
                    letter_count[guess[i]] -= 1
                    self.hint[i] = f'[{guess[i]}]'
                    success = False
                else:
                    self.hint[i] = '_'
                    success = False

            # determine whether to win or lose and leave a hint
            if success:
                return self.win()
            else:
                self.attempts -= 1

                if self.attempts == 0:
                    return self.lose()

                return self.status()

    def status(self) -> str:
        hint = ' '.join(self.hint)

        return (
            f'Number of attempts left: `{self.attempts}`\n'
            f'Hint: `{hint}`'
        )

    def lose(self) -> str:
        self.cleanup()
        return f"You lost! The word was `{self.word}`"

    def win(self) -> str:
        self.cleanup()
        return f"You won! The word was `{self.word}`"

    def cleanup(self):
        self.GAMES[self.channel] = None

class Wordle(DiscordCog):
    @commands.command(name='wordle')
    async def command(self, ctx, *, length: int = 5):
        if WordleGame.get(ctx.channel):
            await ctx.send(content=f'There is a wordle game in this channel already!')
        else:
            try:
                WordleGame(length, ctx.channel)

                await ctx.send(content=f'Wordle game started with word length of `{length}`')
            except ValueError as e:
                await ctx.send(content=f'Error: {e}')

    def help(self):
        return "Starts a game of Wordle with the specified word length. Usage: !wordle #. Use !guess <word> once a game has started to guess the word."

class Guess(DiscordCog):
    @commands.command(name='guess')
    async def command(self, ctx, *, word: str = None):
        game = WordleGame.get(ctx.channel)

        if game:
            # guess word
            guess = game.guess(word)

            await ctx.send(content=f'{guess}')
        else:
            await ctx.send(content=f'There is no active game of Wordle in this channel!')

async def setup(bot):
    await bot.add_cog(Wordle(bot))
    await bot.add_cog(Guess(bot))