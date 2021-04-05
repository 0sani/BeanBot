import discord
from discord.ext import commands

import asyncio

from .timelib import Time, TimeError

class Text(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client


    @commands.command()
    async def echo(self, ctx, *args):
        await ctx.message.delete()
        await ctx.send(" ".join(args))



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

        # If I don't fetch the message again it won't get the emojis
        result = discord.Embed(title=title, description=question, color=discord.Color.purple())
        result.add_field(name="Winner", value=options[int([reaction for reaction in await ctx.fetch_message(message.id).reactions if reaction.me].sort(key=lambda x: x.count, reverse=True)[0].emojis[0]) - 1])
        
        await ctx.send(embed=result)


    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in message.")
        if isinstance(error, TimeError):
            await ctx.send(f"Time input formatted incorrectly.", delete_after=10)


def setup(bot_client):
    bot_client.add_cog(Text(bot_client))