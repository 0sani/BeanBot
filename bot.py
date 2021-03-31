import discord
from discord.ext import commands

import json
import os

from local import discord_token

bot_client = commands.Bot(command_prefix='?')


@bot_client.command()
async def police_mute(ctx, member: discord.Member, reason, muted_role_name):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)

    ## Checks if muted role exists
    if not muted_role:
        await ctx.send(f"Muted role {muted_role_name} does not exist.")
        return

    ## Checks if there are any similar roles between the allowed roles for the muted role and the authors roles
    with open("Info/ServerInfo.json", "r") as json_file:
        json_dict = json.load(json_file)
        if not any(i in ctx.author.roles for i in json_dict["police_mutes"][muted_role.name]):
            await ctx.send(f"You do not have permissions to give people the role {muted_role.name}")
            return

    await member.add_roles(muted_role, reason=reason)
    await member.send(f"You have been muted in {ctx.guild.name} for {reason}.")
    await ctx.send(f"{member.name} has been muted.")


@bot_client.command()
async def get_role(ctx, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    ## Checks if role exists
    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    ## Checks if role is too high in role hierarchy
    try:
        with open("Info/ServerInfo.json", "r") as json_file:
            ctx.guild.roles.index(role, 0, ctx.guild.roles.index(discord.utils.get(ctx.guild.roles, name=json.load(json_file)["highest_get_role"])))
    except ValueError:
        await ctx.send(f"Unable to get role {role.name}, too high in role hierarchy.")
        return

    await ctx.author.add_roles(role)
    await ctx.author.send(f"You have been given the {role.name} role in {ctx.guild.name}.")
    await ctx.send(f"{ctx.author.name} has been given the role {role.name}.")


@bot_client.command()
async def remove_role(ctx, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    # Checks if role exists
    if not role:
        await ctx.send(f"{name} is not a role.")
        return
        
    await ctx.author.remove_roles(role)
    await ctx.author.send(f"The role {role.name} has been removed in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been removed from {ctx.author.name}.")


@bot_client.command()
@commands.has_permissions(administrator=True)
async def give_role(ctx, member: discord.Member, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    ## Checks if role exists
    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    await member.add_roles(role)
    await member.send(f"You have been given the role {role.name} in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been given to {member.name}.")


@bot_client.command()
@commands.has_permissions(administrator=True)
async def take_role(ctx, member: discord.Member, name):
    role = discord.utils.get(ctx.guild.roles, name=name)

    ## Checks if role exists
    if not role:
        await ctx.send(f"{name} is not a role.")
        return

    await member.remove_roles(role)
    await member.send(f"The role {role.name} has been taken in {ctx.guild.name}.")
    await ctx.send(f"The role {role.name} has been taken from {member.name}.")


## Loads a cog; increases bot functionality
@bot_client.command()
@commands.has_permissions(administrator=True)
async def enable_cog(ctx, cog):
    if os.path.isfile(f"./cogs/{cog}"):
        bot_client.load_extension("cogs." + cog)
        await ctx.send(f"Cog {cog} loaded.")
    else:
        await ctx.send(f"Cog {cog} not found.")


## Unloads a cog; decreases bot functionality for current run
@bot_client.command()
@commands.has_permissions(administrator=True)
async def disable_cog(ctx, cog):
    if os.path.isfile(f"./cogs/{cog}"):
        bot_client.unload_extension("cogs." + cog)
        await ctx.send(f"Cog {cog} unloaded.")
    else:
        await ctx.send(f"Cog {cog} not found.")


## Loads all cogs on run
for file_name in os.listdir("./cogs"):
    if file_name.endswith(".py"):
        bot_client.load_extension("cogs." + file_name[:-3])

bot_client.run(discord_token)
