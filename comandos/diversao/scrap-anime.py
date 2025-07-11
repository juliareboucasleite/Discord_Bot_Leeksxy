import discord
from discord.ext import commands

class Scrap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scrap", help="Scrapeia links de anime (simulado)")
    async def scrap(self, ctx, *, texto=None):
        if not texto or ' = ' not in texto:
            return await ctx.send("Uso correto: `'scrap <anime> = <episódio>`")

        anime, episodio = texto.split(" = ")
        anime = anime.strip()
        episodio = episodio.strip()

        await ctx.send("🔍 Buscando links simulados...")

        # Simulando links
        links = [
            ("Gogo Server 1", "https://exemplo.com/servidor1"),
            ("Gogo Server 2", "https://exemplo.com/servidor2"),
            ("MP4Upload", "https://exemplo.com/mp4upload"),
            ("VidStream", "https://exemplo.com/vidstream"),
            ("Backup Link", "https://exemplo.com/backup"),
            ("Mirror", "https://exemplo.com/mirror")
        ]

        embed = discord.Embed(
            title=f"Anime - {anime} | Episódio {episodio}",
            color=discord.Color.random()
        )

        for nome, url in links:
            embed.add_field(name=nome, value=f"[Acessar]({url})", inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Scrap(bot))
