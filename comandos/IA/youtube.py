from discord.ext import commands
from youtubesearchpython import VideosSearch
from typing import Optional

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="youtube", aliases=["yt", "ytsearch"])
    async def youtube(self, ctx, *, query: Optional[str] = None):
        """Busca um vídeo no YouTube e retorna o primeiro resultado."""
        if not query:
            await ctx.send("❌ Você precisa digitar algo para pesquisar!")
            return
        videos_search = VideosSearch(query, limit=1)
        result = videos_search.result()
        if result["result"]:
            video = result["result"][0]
            title = video["title"]
            url = video["link"]
            await ctx.send(f"🔎 **{title}**\n{url}")
        else:
            await ctx.send("❌ Nenhum resultado encontrado no YouTube.")

async def setup(bot):
    await bot.add_cog(Youtube(bot))
