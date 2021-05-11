import discord
from discord.ext import commands 

from .exceptionslib import RoleNotFoundError, RoleTooHighInHierarchyError

class Roles(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client


    @commands.command()
    async def get_role(self, ctx, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
    
        if role is None:
            raise RoleNotFoundError(f"Role {name} not found.")
    
        ## Checks if role is too high in role hierarchy
        if ctx.guild.roles.index(role) >= ctx.guild.roles.index(discord.utils.get(ctx.guild.roles, name="Server Booster")):
            raise RoleTooHighInHierarchyError(role)
    
        await ctx.author.add_roles(role)
        await ctx.author.send(f"You have been given the {role.name} role in {ctx.guild.name}.")
        await ctx.send(f"{ctx.author.name} has been given the role {role.name}.")


    @commands.command()
    async def remove_role(self, ctx, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
    
        if not role:
            raise RoleNotFoundError(f"Role {name} not found.")
            
        await ctx.author.remove_roles(role)
        await ctx.author.send(f"The role {role.name} has been removed in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been removed from {ctx.author.name}.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def give_role(self, ctx, member: discord.Member, name):
        role = discord.utils.get(ctx.guild.roles, name=name)

        if not role:
            raise RoleNotFoundError(f"Role {name} not found.")
    
        await member.add_roles(role)
        await member.send(f"You have been given the role {role.name} in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been given to {member.name}.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def take_role(self, ctx, member: discord.Member, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
    
        if not role:
            raise RoleNotFoundError(f"Role {name} not found.")
    
        await member.remove_roles(role)
        await member.send(f"The role {role.name} has been taken in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been taken from {member.name}.")


    async def cog_command_error(self, ctx, error):
        if isinstance(error, RoleNotFoundError):
            await ctx.send(error.message)
        if isinstance(error, RoleTooHighInHierarchyError):
            await ctx.send(f"Role {error.role} too high in role hierarchy.")
    

def setup(bot_client):
    bot_client.add_cog(Roles(bot_client))
