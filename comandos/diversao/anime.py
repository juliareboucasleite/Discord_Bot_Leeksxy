from discord.ext import commands
import discord
import aiohttp
from typing import Optional

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime", aliases=["kitsu"])
    async def anime(self, ctx, *, nome: Optional[str] = None):
        if not nome:
            await ctx.send("Fale o nome de um anime")
            return
        url = f"https://kitsu.io/api/edge/anime?filter[text]={nome}"
        headers = {
            'Content-Type': "application/vnd.api+json",
            'Accept': "application/vnd.api+json"
        }
        msg = await ctx.send("Procurando informações...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await msg.delete()
                    await ctx.send("Erro ao buscar informações do anime.")
                    return
                data = await resp.json()
                try:
                    anime = data["data"][0]["attributes"]
                    embed = discord.Embed(
                        title=anime["titles"].get("en", nome),
                        description=anime["synopsis"],
                        color=discord.Color.red()
                    )
                    embed.set_thumbnail(url=anime["posterImage"]["original"])
                    embed.add_field(name="Nota", value=anime.get("averageRating", "N/A"))
                    embed.add_field(name="Total de episódios", value=anime.get("episodeCount", "N/A"))
                    if anime.get("coverImage") and anime["coverImage"].get("large"):
                        embed.set_image(url=anime["coverImage"]["large"])
                    await ctx.send(embed=embed)
                except Exception:
                    await ctx.send("Infelizmente eu não achei esse anime")
                await msg.delete()

async def setup(bot):
    await bot.add_cog(Anime(bot))