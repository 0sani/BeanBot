import discord
from discord.ext import commands

class Roles(commands.Cog):

    def __init__(self, client):
        self.client = client

    def findRole(self, roles: list[discord.Role], name: str):

        for role in roles:
            if (role.name.lower() == name.lower()):
                return role
        return None

    @commands.command()
    async def get_role(self, ctx, name):
        role = self.findRole(ctx.guild.roles, name)
        
        if not role:
            await ctx.send(f"{name} not found")
            return

        await ctx.author.add_roles(role)
        await ctx.author.send(f"You have been given the {role.name} role in {ctx.guild.name}.")
        await ctx.send(f"{ctx.author.name} has been given the role {role.name}.")

    @commands.command()
    async def remove_role(self, ctx, name):
        role = self.findRole(ctx.guild.roles, name)
            
        if (not role or name not in [str(x) for x in ctx.author.roles]): # The second condition is really cursed, refactor later
            await ctx.send(f"You do not have {name} or it does not exist") # Can be changed to be more specific about what the issue is
            return
        
        await ctx.author.remove_roles(role)
        await ctx.author.send(f"The role {role.name} has been removed in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been removed from {ctx.author.name}.")


    @commands.command(hidden=True) # Hidden because if normal members use the command then it'd just be clutter
    async def give_role(self, ctx, member: discord.Member, name):
        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(f"You must be an admin to use this command.")
            return

        role = self.findRole(ctx.guild.roles, name)

        if not role:
            await ctx.send(f"{name} not found")
            return

        await member.add_roles(role)
        await member.send(f"You have been given the role {role.name} in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been given to {member.name}.")

    @commands.command(hidden=True) # Hidden because if normal members use the command then it'd just be clutter
    async def take_role(self, ctx, member: discord.Member, name):
        if (not ctx.author.guild_permissions.administrator):
            await ctx.send(f"You must be an admin to use this command.")
            return

        role = self.findRole(ctx.guild.roles, name)

        if (not role or name not in [str(x) for x in member.roles]): # The second condition is really cursed, refactor later
            await ctx.send(f"You do not have {name} or it does not exist")
            return

        await member.remove_roles(role)
        await member.send(f"The role {role.name} has been taken in {ctx.guild.name}.")
        await ctx.send(f"The role {role.name} has been taken from {member.name}.")
