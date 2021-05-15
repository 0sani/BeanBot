import discord
from discord.ext import commands

import asyncio

from .timelib import Time, TimeError

class Text(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client


    @commands.command(rest_is_raw=True)
    async def echo(self, ctx, *, arg):
        if "@here" in arg or "@everyone" in arg:
            return

        await ctx.message.delete()
        await ctx.send(arg)


    @commands.command()
    async def poll(self, ctx, title, question, time: Time, *options):
        if len(options) > 9:
            await ctx.send("Only 9 options allowed.")
            return

        embed = discord.Embed(title=title, description=question, color=discord.Color.purple())
        for i in range(len(options)):
            embed.add_field(name=f"Option {i + 1}", value=options[i])
        message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await message.add_reaction(f"{i + 1}\uFE0F\u20E3")
        
        await asyncio.sleep(time.seconds)

        message = await ctx.fetch_message(message.id) # If I don't fetch the message again it won't get the emojis
        reactions = [reaction for reaction in message.reactions if reaction.me]
        reactions.sort(key=lambda x: x.count, reverse=True)
        index = int(reactions[0].emoji[0])-1

        result = discord.Embed(title=title, description=question, color=discord.Color.purple())
        result.add_field(name="Winner", value=options[index])
        await ctx.send(embed=result)


    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in message.")
        if isinstance(error, TimeError):
            await ctx.send(f"Time input formatted incorrectly.", delete_after=10)


def setup(bot_client):
    bot_client.add_cog(Text(bot_client))
