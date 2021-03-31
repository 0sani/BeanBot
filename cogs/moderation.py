import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot_client):
        self.bot_client = bot_client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, reason="No reason given", muted_role_name="Muted"):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
    
        ## Creates muted role if it doesn't exist
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)
    
        await member.add_roles(muted_role, reason=reason)
        await member.send(f"You have been muted in {ctx.guild.name} for {reason}.")
        await ctx.send(f"{member.name} has been muted.")
        
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member, muted_role_name="Muted"):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
    
        ## Checks if overloaded muted role inputted wrong
        if not muted_role:
            await ctx.send(f"Muted role {muted_role_name} does not exist.")
            return
    
        await member.remove_roles(muted_role)
        await member.send(f"You have been unmuted in {ctx.guild.name}.")
        await ctx.send(f"{member.name} has been unmuted.")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, reason="No reason given"):
        await member.kick(reason=reason)
        await member.send(f"You have been kicked from {ctx.guild.name}.")
        await ctx.send(f"{member.name} has been kicked for {reason}.")


def setup(bot_client):
    bot_client.add_cog(Moderation(bot_client))
