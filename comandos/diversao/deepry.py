import discord
from discord.ext import commands

class DeepFry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="deepfry")
    async def deepfry(self, ctx, *args):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author

        avatar_url = user.display_avatar.with_size(1024).with_format("png")

        embed = discord.Embed(
            title=f"{'Seu' if user == ctx.author else f'O avatar de {user.display_name}'} invertido!",
            color=discord.Color.random()
        )
        embed.set_image(url=f"https://api.alexflipnote.dev/filter/deepfry?image={avatar_url}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DeepFry(bot))
