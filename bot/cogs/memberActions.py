import discord
from discord.ext import commands

class MemberActions(commands.Cog):

    def __init__(self, bot_client):
        self.bot_client = bot_client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
    
        await channel.send(f"Welcome {member.mention} to Beanchat!")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel

        await channel.send(f"{member.mention} left Beanchat :pensive:")

def setup(bot_client):
    bot_client.add_cog(MemberActions(bot_client))