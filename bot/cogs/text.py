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

        #due to emoji limitations polls will be limited to 10 options
        if (len(options) > 10):
            await ctx.send("Too many arguments, 10 is the maximum number of options")
            return

        embed = discord.Embed(title=title, description=question, color=discord.Color.purple())

        for i in range(len(options)):
            embed.add_field(name=f"Option {i+1}", value = options[i])
        
        await ctx.send(embed=embed)
        await asyncio.sleep(time.seconds)
        await ctx.send("Poll complete")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in message.")
        if isinstance(error, TimeError):
            await ctx.send(f"Time input formatted incorrectly.", delete_after=10)


def setup(bot_client):
    bot_client.add_cog(Text(bot_client))