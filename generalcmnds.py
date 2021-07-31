import discord
from discord.ext import commands
import random

console_chat = 870970958222078012
welcome_chat = 871018758469210143
rules_chat = 864475213097992242

eight_ball_answers = ['Most definitely.',
'Yes.', 'Absolutely!', 'The signs say yes', 'Without a doubt!',
'I am not sure...', 'Hazy answer; try again',
'Nope!', 'Outlook not so good', 'The weather suggests no.', 'Absolutely not!', 'Very doubtful']

class generalcmnds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(member_name + " has been unbanned")
                return
        await ctx.send(member+" was not found")


    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, message):
        embed = discord.Embed(title=ctx.channel, description=message)
        await ctx.channel.send(embed=embed)


    @commands.command(name="8ball")
    async def eight_ball(self, ctx):
        await ctx.channel.send(random.choice(eight_ball_answers))


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, messages=5):
        await ctx.channel.purge(limit=messages)


def setup(client):
    client.add_cog(generalcmnds(client))
