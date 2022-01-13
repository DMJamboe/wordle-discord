# module containing all bot commands

import discord
from discord.ext import commands
from discord.embeds import Embed
from gamemanager import GameManager, Game, Guess
from wordmanager import WordManager

guild_ids=[931281545933762571]

def load(bot: commands.Bot):
    @bot.slash_command(guild_ids=guild_ids)
    async def about(ctx: commands.Context):
        mbd = Embed()
        mbd.title = "WordJam"
        mbd.description = "A discord bot emulating the game Wordle."
        mbd.add_field(name="Version", value="Alpha 1")
        await ctx.respond(embed=mbd)

    @bot.slash_command(guild_ids=guild_ids)
    async def random(ctx: commands.Context):
        if GameManager.hasGame(ctx.author):
            await ctx.respond("Game already ongoing.")
        else:
            await GameManager.createGame(ctx.author)
            await ctx.respond("Game started.")

    @bot.command()
    async def guess(ctx: commands.Context, guess: str.lower):
        if isinstance(ctx.channel, discord.DMChannel):
            if GameManager.hasGame(ctx.author):
                game = GameManager.getGame(ctx.author)
                response = game.makeGuess(guess)
                if response is None:
                    await ctx.send("Invalid guess.")
                else:
                    readableResponse = "".join([Guess.getEmoji(guess) for guess in response])
                    fullResponse = f"Guess {game.numGuesses()}/{game.maxRounds} - {guess}\n{readableResponse}"
                    await ctx.send(fullResponse)

                if game.isLost():
                    GameManager.gameEnd(game)
                    await ctx.send(f"Game Over.\nThe word was: {game.word}")

                if game.word == guess:
                    GameManager.gameEnd(game)
                    await ctx.send(f"Congratulations!\nThe word was: {game.word}")

            else:
                await ctx.send(content="No game has been started.")

    @bot.command()
    async def random(ctx: commands.Context):
        if isinstance(ctx.channel, discord.DMChannel):
            if GameManager.hasGame(ctx.author):
                await ctx.respond("Game already ongoing.")
            else:
                await GameManager.createGame(ctx.author)
            