import discord
from discord.ext import commands
import os

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")

class Venda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="venda", aliases=["vendask"])
    async def venda(self, ctx, *, texto=None):
        if str(ctx.author.id) not in OWNER_IDS:
            return await ctx.send("🔒 Apenas meu desenvolvedor pode usar esse comando.")

        if not texto or " / " not in texto:
            return await ctx.send(
                "❗ Use o formato: `'venda <título> / <anúncio>'`\nExemplo: `'venda Monitor Gamer / 144Hz Full HD por 99€`"
            )

        titulo, anuncio = map(str.strip, texto.split(" / ", 1))

        embed = discord.Embed(
            color=discord.Color.orange()
        )
        embed.add_field(name=f"📢 Título: {titulo}", value=f"📝 **Informação do Produto:** {anuncio}", inline=False)
        embed.set_footer(text=f"Anúncio feito por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        embed.timestamp = discord.utils.utcnow()

        await ctx.message.delete()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Venda(bot))
