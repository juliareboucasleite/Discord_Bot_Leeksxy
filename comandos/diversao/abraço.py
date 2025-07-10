import discord
from discord.ext import commands
import aiohttp
import random
from typing import Optional

class Abraco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="abraco", aliases=["abraço", "hug", "abracar"])
    async def abracar_command(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
            "https://c.tenor.com/P4z6y1PjC5wAAAAC/anime-hug.gif",
            "https://c.tenor.com/p917G_R_c7QAAAAC/peach-goma-hug.gif",
            "https://c.tenor.com/S6-J_42FzXkAAAAC/goma-peach-hug.gif",
            "https://c.tenor.com/k4p3YF_84tIAAAAC/gif-hug.gif",
            "https://c.tenor.com/I3u1rNfM700AAAAC/hug-anime-hug.gif",
            "https://c.tenor.com/QjBqZ71l5YgAAAAC/hug-anime.gif",
            "https://c.tenor.com/iJ6qg8C3-oAAAAAC/hug-cuddle.gif",
            "https://c.tenor.com/tC6F9_vGj04AAAAC/kiss-anime.gif",
            "https://c.tenor.com/9l89nLq-RzQAAAAC/dias-de-escola-beijo.gif",
            "https://c.tenor.com/n1h8yW4T-lQAAAAC/anime-couple-love.gif",
            "https://c.tenor.com/9xS76mPgaEIAAAAC/milk-and-mocha-bear-couple.gif",
            "https://c.tenor.com/0iKj4SgG9YMAAAAC/love-anime.gif"
        ]

        # Tenta pegar GIF da API waifu.pics
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/hug") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data["url"]
                    else:
                        gif_url = random.choice(gifs)
        except Exception:
            gif_url = random.choice(gifs)

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem abraçar?",
                description="Por favor, mencione um membro para dar um abraço!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😊 Awn, obrigado!",
                description="Obrigado por me abraçar! Fico feliz em receber carinho!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🙃 Auto Abraço",
                description="Você se abraçou sozinho... É fofo e um pouco triste ao mesmo tempo!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="🤗 Abraço Recebido!",
            description=f"{ctx.author.mention} deu um abraço apertado em {membro.mention}!",
            color=0xE8E8E8
        )
        embed.set_image(url=gif_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Sinta o carinho!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Abraco(bot))
