import discord
from discord.ext import commands
import random
from typing import Optional

class LamberView(discord.ui.View):
    def __init__(self, autor, alvo):
        super().__init__(timeout=60)
        self.autor = autor
        self.alvo = alvo

    @discord.ui.button(label="👅 Lamber de volta", style=discord.ButtonStyle.secondary)
    async def lamber_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.alvo.id:
            embed = discord.Embed(
                title="❌ Não é sua vez!",
                description=f"Apenas {self.alvo.mention} pode retribuir o beijo!",
                color=0xE8E8E8
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        gifs = [
            'https://media.tenor.com/1oHjFb8iKGIAAAAC/lick-anime.gif',
            'https://media.tenor.com/1ChcN3szUGkAAAAC/lick-licking.gif',
            'https://media.tenor.com/zkVq_fXwM4wAAAAC/lick-anime-kiss.gif',
            'https://media.tenor.com/F0r0p_Y0_LAAAAAC/lick-anime-cute.gif',
            'https://media.tenor.com/gK9e4H_2m9QAAAAC/lick-cute.gif',
            'https://cdn.nekotina.com/images/OnFejF0Zi.gif',
            'https://cdn.nekotina.com/images/ZR7TmCXE.gif'
        ]

        embed = discord.Embed(
            title="👅 Lamber de Volta!",
            description=f"{self.alvo.mention} lambeu {self.autor.mention} de volta!",
            color=0xE8E8E8
        )
        embed.set_image(url=random.choice(gifs))
        embed.set_author(name=self.alvo.display_name, icon_url=self.alvo.avatar.url if self.alvo.avatar else None)
        embed.set_footer(text="Que divertido!")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed)
        self.stop()

class Lamber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lamber", aliases=["lick"])
    async def lamber_command(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
            "https://c.tenor.com/3.gif",
            "https://c.tenor.com/4.gif"
            # Adicione mais GIFs locais se quiser
        ]

        # Tenta pegar GIF da API waifu.pics
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/lick") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data["url"]
                    else:
                        gif_url = random.choice(gifs)
        except Exception:
            gif_url = random.choice(gifs)

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem lamber?",
                description="Por favor, mencione um membro para lamber!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Ei!",
                description="Por que está tentando me lamber? Eu sou só um bot!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🙃 Auto Lambida",
                description="Você se lambeu... Isso foi estranho!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="👅 Lambida!",
            description=f"{ctx.author.mention} lambeu {membro.mention}!",
            color=0xE8E8E8
        )
        embed.set_image(url=gif_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Isso foi estranho!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lamber(bot))