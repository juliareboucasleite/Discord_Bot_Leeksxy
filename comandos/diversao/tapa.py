import discord
from discord.ext import commands
import random

class Tapa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tapa", aliases=["slap", "bater"], help='Dá um tapa em um membro. Uso: \'tapa <@membro>')
    async def tapa(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()

        gifs = [
            'https://media.tenor.com/Vj-1Ez4-eQQAAAAC/anime-slap.gif',
            'https://media.tenor.com/KFi0N6BBkyoAAAAC/slap-anime.gif',
            'https://media.tenor.com/eIRAcj0RIdkAAAAC/anime-slap.gif'
        ]

        if not membro:
            return await ctx.send("🖐️ Você precisa mencionar alguém para dar um tapa!")

        if membro.id == self.bot.user.id:
            return await ctx.send("😤 Quer me dar um tapa? Tome! https://tenor.com/view/slap-bears-gif-10422113")

        if membro.id == ctx.author.id:
            return await ctx.send("🥊 Ixi... Quero ver você se batendo sozinho então...")

        embed = discord.Embed(
            title=f"tapa {ctx.author.display_name}",
            description=f"{ctx.author.mention} acaba de dar um tapa em {membro.mention}! 🖐️",
            color=0x000000
        )
        embed.set_image(url=random.choice(gifs))
        embed.set_footer(text="Ui! Essa foi feia... Ai...")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.timestamp = discord.utils.utcnow()

        msg = await ctx.send("<a:loading:766632994249113602> carregando...")
        await msg.edit(content=f"{ctx.author.mention}", embed=embed)
        await msg.delete(delay=10)

async def setup(bot):
    await bot.add_cog(Tapa(bot))
# Note: This code defines a Discord bot command that allows users to "slap" other members with a random GIF.