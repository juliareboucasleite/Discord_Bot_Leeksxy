import discord
from discord.ext import commands
import aiohttp
import random
from typing import Optional

class Cuddle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cuddle", aliases=["carinho", "acariciar", "afagar"], help='Faz carinho em um membro. Uso: \'cuddle <@membro>')
    async def cuddle(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        # Lista de GIFs de carinho (você pode adicionar mais se desejar)
        gifs = [
            'https://media.giphy.com/media/GPMkK3wWv0E0hM0X3f/giphy.gif', # Exemplo de gif de carinho
            'https://media.tenor.com/images/c6f5d8a0c201d4b6b1a3e6f9b1f2e6e3/tenor.gif',
            'https://media.tenor.com/images/15053158c89b708298717904085b46e3/tenor.gif'
        ]

        # Tenta obter um GIF da API nekos.life
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://nekos.life/api/v2/img/cuddle") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data["url"]
                    else:
                        gif_url = random.choice(gifs) # Fallback para lista local se a API falhar
        except Exception:
            gif_url = random.choice(gifs) # Fallback para lista local se houver erro na requisição

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem acariciar?",
                description="Por favor, mencione um membro para dar carinho!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="🤗 Awn, que carinho!",
                description="Obrigado(a) por me dar carinho! Adoro receber afeto!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="💖 Auto Carinho!",
                description="Você está se dando um pouco de amor. Que fofo!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="🐾 Carinho no Ar!",
            description=f"{ctx.author.mention} fez um carinho gostoso em {membro.mention}! Que momento fofo! 🥺",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        embed.set_image(url=gif_url)
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Sinta o amor e a fofura!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cuddle(bot))
