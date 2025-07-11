from discord.ext import commands
import discord
from googlesearch import search
from typing import Optional

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="google", aliases=["g"])
    async def google(self, ctx, *, query: Optional[str] = None):
        """Busca no Google e retorna os 5 primeiros resultados."""
        if not query:
            await ctx.send("❌ Você precisa digitar algo para pesquisar!")
            return
        try:
            results = list(search(query, num_results=5, lang="pt"))
            if not results:
                await ctx.send("❌ Não encontrei resultados para sua busca.")
                return
            embed = discord.Embed(
                title=f"Resultados para: {query}",
                color=0x4285F4
            )
            for i, link in enumerate(results, 1):
                embed.add_field(name=f"Resultado {i}", value=link, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro!\n{e}")

async def setup(bot):
    await bot.add_cog(Google(bot))