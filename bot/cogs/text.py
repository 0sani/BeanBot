import discord
from discord.ext import commands

from .timelib import Time, TimeError

class Text(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client


    @commands.command()
    async def echo(self, ctx, *args):
        await ctx.message.delete()
        await ctx.send(" ".join(args))


    ## Dont work idot
    @commands.command()
    async def poll(self, ctx, title, question, option1, option2, time: Time):
        embed = discord.Embed(title=title, description=question, color=discord.Color.purple)
        embed.add_field(name="Option 1", value=option1)
        embed.add_field(name="Option 2", value=option2)

        await ctx.send(embed=embed)


    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in message.")
        if isinstance(error, TimeError):
            await ctx.send(f"Time input formatted incorrectly.", delete_after=10)


def setup(bot_client):
    bot_client.add_cog(Text(bot_client))