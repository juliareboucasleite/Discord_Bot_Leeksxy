import discord
from discord.ext import commands
from typing import Optional

class Pixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pixel", aliases=["pixelado"])
    async def pixel(self, ctx, member: Optional[discord.Member] = None):
        member = member or ctx.author
        avatar_url = member.display_avatar.with_size(1024).with_format("png")
        pixel_url = f"https://api.alexflipnote.dev/filter/pixelate?image={avatar_url}"

        embed = discord.Embed(
            title=f"{member.display_name} avatar pixelado!",
            color=discord.Color.random()
        )
        embed.set_image(url=pixel_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pixel(bot))