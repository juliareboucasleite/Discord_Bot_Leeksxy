import discord
from discord.ext import commands
from typing import Optional

class Sepia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sepia", aliases=["marrom"])
    async def sepia(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        avatar_url = member.display_avatar.with_size(1024).with_format("png")
        sepia_url = f"https://api.alexflipnote.dev/filter/sepia?image={avatar_url}"

        embed = discord.Embed(
            title=f"{member.display_name} com efeito sépia!",
            color=discord.Color.random()
        )
        embed.set_image(url=sepia_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Sepia(bot))