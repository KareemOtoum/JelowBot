import discord
from discord.ext import commands
from pymongo import MongoClient
import random

bot_channel = [834005757846487050, 864474885807276063]
talk_channels = [864474885807276063, 834005261634764843, 834005335681269770, 834005432372559893, 865948592484515860, 865948592484515860]

level = ["Base", "Super Saiyan", "Super Saiyan 2", "Super Saiyan 3", "Super Saiyan God", "Super Saiyan Blue",
         "Super Saiyan Rose", "Legendary Super Saiyan", "Ultra Instinct", "Mastered Ultra Instinct"]
levelnum = [2, 5, 8, 12, 15, 20, 25, 30, 40, 50]

cluster = MongoClient("")

levelling = cluster["discord"]["levelling"]

dbz_gifs = ['https://media.giphy.com/media/cb9aF9tDyiRkYbz3BX/giphy.gif',
            'https://media.giphy.com/media/U3UP4fTE6QfuoooLaC/giphy.gif',
            'https://media.giphy.com/media/mG1uA7JnuAZqbWV44g/giphy.gif',
            'https://media.giphy.com/media/RT8t27SY5rRVfF5MJw/giphy.gif']

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id" : message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id" : message.author.id, "name" : message.author.name + "#" + message.author.discriminator, "xp" : 0, "warnings" : 0}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2)) + (50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2)) + (50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"{message.author.mention} Leveled up to **level {lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention} has achieved **{level[i]}** form!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                embed.colour = discord.Colour.blue()
                                await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id in bot_channel:
            stats = levelling.find_one({"id" : ctx.author.id})
            if stats is None:
                embed = discord.Embed(description="You haven't sent any messages yet, you have no rank :pensive:")
                embed.colour = discord.Colour.blue()
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
                boxes = int((xp/(200*((1/2) * lvl))) *20)
                rankings = levelling.find().sort("xp",-1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(title=f"{ctx.author.name}'s level stats")
                embed.add_field(name=":bust_in_silhouette:Name", value=ctx.author.mention, inline=True)
                embed.add_field(name=":sparkles:XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name=":medal:Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name=f"Progress Bar **[level:{lvl}]**", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.colour = discord.Colour.blue()
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id in bot_channel:
            rankings = levelling.find().sort("xp",-1)
            i = 1
            embed = discord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    embed.colour = discord.Colour.blue()
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


    @commands.command()
    async def roles(self, ctx):
        if ctx.channel.id in bot_channel:
            embed = discord.Embed(title="**Roles**")
            embed.add_field(name="Role names:", value=" | ".join(i for i in level), inline=True)
            embed.add_field(name="Amount of Roles: ", value=len(level), inline=False)
            embed.colour = discord.Colour.blue()
            embed.set_image(url=random.choice(dbz_gifs))
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levelsys(client))
