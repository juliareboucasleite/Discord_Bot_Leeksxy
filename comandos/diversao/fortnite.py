import discord
from discord.ext import commands

class Fortnite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fortnite")
    async def fortnite(self, ctx):
        embed = discord.Embed(
            color=discord.Color.red()
        )
        embed.set_image(url="https://ctk-api.herokuapp.com/fortnite-shop")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fortnite(bot))
