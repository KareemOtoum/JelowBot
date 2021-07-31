import discord
from discord.ext import commands
from pymongo import MongoClient
import spamdetect
import asyncio

cluster = MongoClient("mongodb+srv://Jelow:Mesho321@cluster0.q8izt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["discord"]["levelling"]

blacklist = ['cunt', 'chigg', 'chink', 'coon', 'cuck', 'fag',
             'hentai', 'minge', 'n1bb', 'n1gg', 'negro', 'nibb', 'nlbb', 'nigg',
             'nlgg', 'nonce', 'pedo', 'savile', 'retard', 'slut', 'whore', 'porn']

class filtering(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(blacklist)):
            if blacklist[i] in message.content and not message.author.bot:
                stats = levelling.find_one({"id": message.author.id})
                channel = await message.author.create_dm()

                if stats is None:
                    newuser = {"id": message.author.id, "xp": 0, "warnings": 1}
                    levelling.insert_one(newuser)
                else:
                    warnings = stats["warnings"] + 1
                    levelling.update_one({"id": message.author.id}, {"$set": {"warnings": warnings}})

                stats = levelling.find_one({"id": message.author.id})

                if stats["warnings"] < spamdetect.warnings_until_ban:
                    embed = discord.Embed(title="""```YOU WERE KICKED```""",
                                          description=f"You were kicked from [Jelow's Fever Dream](https://discord.gg/2shCvEck5F) \n(READ THE RULES BEFORE REJOINING) \n"
                                                      f"this is regarding your following message:\n\n"
                                                      f"```{message.content}```\n\n"
                                                      "your message contained a word that is in the [blacklisted list of words](https://docs.google.com/document/d/1k2p-NRMpW7Q6jZRjJbED93MbewFYbGVv_eoxP6PANvE/edit?usp=sharing)\n"
                                                      "***IF YOU DO THIS AGAIN YOU'LL BE BANNED FROM THE SERVER***")
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
                    await message.guild.ban(message.author, reason="Saying a blacklisted word")

                await message.delete()

def setup(client):
    client.add_cog(filtering(client))