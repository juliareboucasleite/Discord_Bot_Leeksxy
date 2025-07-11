import discord
from discord.ext import commands
import random
from typing import Optional

class Mordida(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mordida", aliases=["bite", "morder"], help="Dá uma mordida em um membro. Uso: 'mordida <@membro>")
    async def mordida(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
            'https://images-ext-1.discordapp.net/external/BeZJf4R7Q-ijwKzZLLee9xvuYhvKCnTU2rNl7OPbc0I/https/cdn.nekotina.com/images/kn_7eAoh.gif?width=362&height=327',
            'https://images-ext-1.discordapp.net/external/Ay4IumDWdtn7huxlyAnKpO1hB4VhGtLsq_f-SRjLiJE/https/cdn.nekotina.com/images/JAbkdhDO.gif?width=335&height=188',
            'https://images-ext-1.discordapp.net/external/KpXTSMehycBQjyEOgFBZ_7ROZY3MWe_uaB-k5PC1PLc/https/media.tenor.com/htI5TkSvyYEAAAPo/cute-anime.mp4',
            'https://images-ext-1.discordapp.net/external/RcCmpQldMMT3DopdZSmaYfUkqMDg5zS_NDOy9xs_bJA/https/media.tenor.com/48DDFOcNQBYAAAPo/anime-bite.mp4',
            'https://images-ext-1.discordapp.net/external/cEIlHG7n1xr2mpSzvd5z6jSln2vTU_KvtOCVAN2k5jM/https/media.tenor.com/n__KGrZPlQEAAAPo/bite.mp4',
            'https://images-ext-1.discordapp.net/external/UAaJKfRZVz5tQjFoOON7wcZvG1X0DyQM2eOZosFrUg0/https/media.tenor.com/JEuY0WWcguIAAAPo/anime-bite.mp4',
            'https://images-ext-1.discordapp.net/external/YqIaZK-EAfEwcamztgrdctJwkvmxaoKjlLFL9bya6dQ/https/media.tenor.com/1LtA9dSoAIQAAAPo/zero-no-tsukaima-bite.mp4',
            'https://images-ext-1.discordapp.net/external/AcjtXiq1TR5iskG_gSuDSA5xDhx_yKJB4Os7LDlkzHI/https/media.tenor.com/0uRmrUvyZFEAAAPo/vamp-vampire-bite.mp4',
            'https://images-ext-1.discordapp.net/external/fErHevCXzTruAMaQ4HkSYi21iSuyJfox0vCXUqMObgA/https/media.tenor.com/hwCVSWyji0QAAAPo/anime-bite.mp4'

        ]

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem morder?",
                description="Por favor, mencione um membro para morder!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Opa!",
                description="Você quer me morder? Ai! Eu sou só um bot, pega leve!",
                color=0xE8E8E8
            )
            embed.set_image(url=random.choice(gifs))
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🪞 Mordendo a Si Mesmo?",
                description="Você tentou se morder... Isso deve doer!",
                color=0xE8E8E8
            )
            embed.set_image(url=random.choice(gifs))
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="😈 Mordida!",
            description=f"{ctx.author.mention} deu uma mordida em {membro.mention}! Ai, cuidado! 🦷",
            color=0xE8E8E8
        )
        embed.set_image(url=random.choice(gifs))
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Cuidado com as mordidas!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mordida(bot))
