import discord
from discord.ext import commands
import random
from typing import Optional

class Tapa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tapa", aliases=["slap", "bater"])
    async def tapa_command(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
         'https://imgur.com/1tEHNcK.gif',
        'https://imgur.com/GSlsYO1.gif',
        'https://imgur.com/mji8DpH.gif'
        ]

        # Tenta pegar GIF da API waifu.pics
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/slap") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data["url"]
                    else:
                        gif_url = random.choice(gifs)
        except Exception:
            gif_url = random.choice(gifs)

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem bater?",
                description="Por favor, mencione um membro para dar um tapa!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Ei!",
                description="Por que está tentando me bater? Eu sou só um bot!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🙃 Auto Tapa",
                description="Você se deu um tapa... Isso foi estranho!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="👋 Tapa!",
            description=f"{ctx.author.mention} deu um tapa em {membro.mention}!",
            color=0xE8E8E8
        )
        embed.set_image(url=gif_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Isso deve ter doído!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tapa(bot))
# Note: This code defines a Discord bot command that allows users to "slap" other members with a random GIF.