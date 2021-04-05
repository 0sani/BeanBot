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
        
        message = await ctx.send(embed=embed)

        emojis = [ # I hate this solution, but it works. Would much rather have unicode escape characters but tired of fighting them
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟"
        ]

        for i in range(len(options)):
            await message.add_reaction(emojis[i])
        
        await asyncio.sleep(time.seconds)

        message = await ctx.fetch_message(message.id) # If I don't fetch the message again it won't get the emojis

        reactions = [reaction for reaction in message.reactions if reaction.me]
        
        reactions.sort(key=lambda x: x.count, reverse=True)

        index = emojis.index(reactions[0].emoji)

        result = discord.Embed(title=title, description=question, color=discord.Color.purple())
        result.add_field(name="Winner", value = options[index])
        
        await ctx.send(embed=result)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.UnexpectedQuoteError):
            await ctx.send("Unexpected quote in message.")
        if isinstance(error, TimeError):
            await ctx.send(f"Time input formatted incorrectly.", delete_after=10)


def setup(bot_client):
    bot_client.add_cog(Text(bot_client))