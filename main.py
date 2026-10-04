from discord.ext import commands
import discord
import levelsys
import music
import filtering
import generalcmnds
import spamdetect

cogs = [levelsys, music, filtering, generalcmnds, spamdetect]

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

has_released_hinterkaifeck = False

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permissions for that command!")

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member):
    muted_role = ctx.guild.get_role(870387279896657960)
    await member.add_roles(muted_role)
    await ctx.channel.purge(limit=1)

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member:discord.Member):
    muted_role = ctx.guild.get_role(870387279896657960)
    await member.remove_roles(muted_role)
    await ctx.channel.purge(limit=1)

@client.event
async def on_member_join(member):
    channel = member.guild.get_channel(generalcmnds.welcome_chat)
    await channel.send("Hello " + member.mention + f" welcome to the server make sure you read the {member.guild.get_channel(generalcmnds.rules_chat).mention} bozo :joy:!")
    if not has_released_hinterkaifeck:
        await member.add_roles(discord.utils.get(member.guild.roles, name="OG Member"))


client.run("")
