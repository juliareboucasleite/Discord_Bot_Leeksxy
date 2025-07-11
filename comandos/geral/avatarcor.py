import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar", aliases=["foto", "icon", "pfp"])
    async def avatar(self, ctx):
        if not ctx.message.mentions:
            return await ctx.send("👤 Ninguém mencionado.")

        for user in ctx.message.mentions:
            embed = discord.Embed(
                title=f"Avatar de {user.display_name}",
                color=discord.Color.random()
            )
            embed.set_image(url=user.display_avatar.replace(size=1024).url)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))
