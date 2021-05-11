import discord
from discord.ext import commands

import os

# Allows member events to work
intents = discord.Intents.all()
bot_client = commands.Bot(command_prefix='?', intents=intents)


## Loads a cog; increases bot functionality
@bot_client.command()
@commands.has_permissions(administrator=True)
async def enable_cog(ctx, cog_name):
    if cog_name.endswith("lib.py") or not os.path.isfile(f"./cogs/{cog_name}") or file_name == "__init__.py":
        await ctx.send(f"Cog {cog_name} not found.", delete_after=10)
    else:
        bot_client.load_extension("cogs." + cog_name)
        await ctx.send(f"Cog {cog_name} enabled.")


## Unloads a cog; decreases bot functionality for current run
@bot_client.command()
@commands.has_permissions(administrator=True)
async def disable_cog(ctx, cog_name):
    if cog_name.endswith("lib.py") or not os.path.isfile(f"./cogs/{cog_name}") or file_name == "__init__.py":
        await ctx.send(f"Cog {cog_name} not found.", delete_after=10)
    else:
        bot_client.unload_extension("cogs." + cog_name)
        await ctx.send(f"Cog {cog_name} disabled.")


## Loads all cogs on run
for file_name in os.listdir("./bot/cogs"):
    if file_name.endswith(".py") and not file_name.endswith("lib.py") and file_name != "__init__.py":
        bot_client.load_extension("cogs." + file_name[:-3])

bot_client.run(os.getenv("BEAN_BOT_TOKEN"))
