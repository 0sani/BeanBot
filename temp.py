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