# OverStats
# Work with Python 3.7.3 Linux

import aiohttp
import json
import discord
from discord.ext import commands

class OverStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Overwatch Profile
    @commands.command(description='Show Overwatch Profile')
    async def profile(self, ctx, battletag : str=None):
        if battletag is None:
            await ctx.send("Please input BattleTag.")
        else:
            url = 'https://ovrstat.com/stats/pc/kr/{}'.format(battletag)

            # Async HTTP request
            async with aiohttp.ClientSession() as session:
                raw_response = await session.get(url)
                response = await raw_response.text()
                data = json.loads(response)

                if 'message' not in data:
                    icon = data['icon']
                    embed = discord.Embed(color=0x7289da)
                    embed.set_author(name=battletag + "'s Profile", icon_url=icon)

                    if data['private'] == True:
                        embed.add_field(name="Error", value="This profile is private", inline=True)
                    else:
                        playtime = data['competitiveStats']['careerStats']['allHeroes']['game']['timePlayed']
                        rating = data['rating']
                        rateicon = data['ratingIcon']
                        endorsement = data['endorsement']

                        embed.set_thumbnail(url=rateicon)
                        embed.add_field(name="Current Season Rating", value=rating, inline=True)
                        embed.add_field(name="Competitive Playtime", value=playtime, inline=True)
                        embed.add_field(name="Endorsement Level", value=endorsement, inline=True)
                else:
                    embed = discord.Embed(title=battletag + "'s Profile", color=0x7289da)
                    embed.add_field(name="Error", value="Player not found", inline=True)

                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OverStats(bot))