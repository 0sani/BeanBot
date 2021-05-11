import discord
from discord.ext import commands

import json, os

# Allows member events to work
intents = discord.Intents.default()
intents.members = True

bot_client = commands.Bot(command_prefix='?', intents=intents)


@bot_client.command()
async def police_mute(ctx, member: discord.Member, reason, muted_role_name):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)

    ## Checks if muted role exists
    if not muted_role:
        await ctx.send(f"Muted role {muted_role_name} does not exist.")
        return

    ## Checks if there are any similar roles between the allowed roles for the muted role and the authors roles
    with open(".info/serverinfo.json", "r") as json_file:
        json_dict = json.load(json_file)
        if not any(i in ctx.author.roles for i in json_dict["police_mutes"][muted_role.name]):
            await ctx.send(f"You do not have permissions to give people the role {muted_role.name}")
            return

    await member.add_roles(muted_role, reason=reason)
    await member.send(f"You have been muted in {ctx.guild.name} for {reason}.")
    await ctx.send(f"{member.name} has been muted.")


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
