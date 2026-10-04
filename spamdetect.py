import discord
from discord.ext import commands
import asyncio
from pymongo import MongoClient

message_limit = 3
warnings_until_ban = 2

cluster = MongoClient("")

levelling = cluster["discord"]["levelling"]

class generalcmnds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            print("cleared")
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as file:
                file.truncate(0)

    @commands.Cog.listener()
    async def on_message(self, message):
        counter = 0
        with open("spam_detect.txt", "r+") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1

            file.writelines(f"{str(message.author.id)}\n")
            if counter > message_limit and not message.author.bot:
                channel = await message.author.create_dm()
                stats = levelling.find_one({"id": message.author.id})
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 0, "warnings": 1}
                    levelling.insert_one(newuser)
                else:
                    warnings = stats["warnings"] + 1
                    levelling.update_one({"id":message.author.id}, {"$set":{"warnings":warnings}})

                stats = levelling.find_one({"id": message.author.id})

                if stats["warnings"] < warnings_until_ban:
                    embed = discord.Embed(title="""```YOU WERE KICKED```""",
                                          description=f"You have been kicked from [Jelow's Fever Dream Server](https://discord.gg/2shCvEck5F)\n"
                                                      f"this is regarding your following spammed message:\n\n"
                                                      f"```{message.content}```\n\n"
                                                      "You were spamming in the server and that is not allowed as said in **rule 1**\n"
                                                      "***IF YOU BREAK THE RULES AGAIN YOU'LL BE BANNED FROM THE SERVER***\n")
                    embed.colour = discord.Colour.red()
                    embed.set_thumbnail(url=message.guild.icon_url)
                    await channel.send(embed=embed)
                    await message.guild.ban(message.author)
                    await asyncio.sleep(1)
                    await message.guild.unban(message.author)
                else:
                    embed = discord.Embed(title="""```YOU HAVE BEEN BANNED```""",
                                          description=f"You have been banned from [Jelow's Fever Dream](https://discord.gg/2shCvEck5F)\n"
                                                      f"this is regarding your following spammed message:\n\n"
                                                      f"```{message.content}```\n\n"
                                                      "You have broken the rules in the server TWICE\n"
                                                      "***To appeal your ban send a message to Jelow#0345 or Feign#7113***\n")
                    embed.colour = discord.Colour.red()
                    embed.set_thumbnail(url=message.guild.icon_url)
                    levelling.delete_one(stats)
                    await channel.send(embed=embed)
                    await message.guild.ban(message.author, reason="Spamming")


def setup(client):
    client.add_cog(generalcmnds(client))
