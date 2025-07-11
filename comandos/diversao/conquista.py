import discord
from discord.ext import commands

class Conquista(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="conquista", aliases=["xreward", "xReward", "xboxReward"])
    async def conquista(self, ctx, *, texto=None):
        if not texto or '+' not in texto:
            await ctx.send("O que deve aparecer na conquista?? (use: `'conquista título + subtítulo`)")
            return

        partes = texto.split("+")
        if len(partes) < 2:
            await ctx.send("O que deve aparecer na conquista??")
            return

        titulo = partes[0].strip()
        subtitulo = partes[1].strip()
        avatar_url = ctx.author.display_avatar.with_format("png")

        imagem_url = f"http://www.achievement-maker.com/xbox/{titulo}?header={subtitulo}&email={avatar_url}.png"

        embed = discord.Embed(
            title="Conquista desbloqueada!!",
            color=discord.Color.gold()
        )
        embed.set_image(url=imagem_url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Conquista(bot))
