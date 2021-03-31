import discord
from discord.ext import commands

import json

from local import discord_token

bot_client = commands.Bot(command_prefix='?')


@bot_client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, reason="No reason given", muted_role_name="Muted"):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)

    ## Creates muted role if it doesn't exist
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)

    await member.add_roles(muted_role, reason=reason)
    await member.send(f"You have been muted in {ctx.guild.name} for {reason}.")
    await ctx.send(f"{member.name} has been muted.")
    

@bot_client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, muted_role_name="Muted"):
    muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)

    ## Checks if overloaded muted role inputted wrong
    if not muted_role:
        await ctx.send(f"Muted role {muted_role_name} does not exist.")
        return

    await member.remove_roles(muted_role)
    await member.send(f"You have been unmuted in {ctx.guild.name}.")
    await ctx.send(f"{member.name} has been unmuted.")


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
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, reason="No reason given"):
    await member.kick(reason=reason)
    await member.send(f"You have been kicked from {ctx.guild.name}.")
    await ctx.send(f"{member.name} has been kicked for {reason}.")


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


bot_client.run(discord_token)
