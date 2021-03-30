import discord
from discord.ext import commands
from datetime import datetime

from local import discord_token
from cogs.roles import Roles


bot_client = commands.Bot(command_prefix='?')

@bot_client.event
async def on_ready():
    print(f"Bot started at {datetime.now()}")

@bot_client.event
async def on_message(msg):

    # This is a test to see if you read through your PRs Doggo
    if ("Osani" in msg.content):
        print("All hail Osani")

    await bot_client.process_commands(msg)

bot_client.add_cog(Roles(bot_client))

bot_client.run(discord_token)
