import discord
from discord.ext import commands
from .utils import now_playing

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resume", aliases=["continuar", "unpause"])
    async def resume_command(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_paused():
            embed = discord.Embed(
                title="❌ Nada Pausado",
                description="Não há nenhuma música pausada para retomar.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if vc.is_playing():
            embed = discord.Embed(
                title="⚠️ Já Tocando",
                description="A música já está tocando.",
                color=0xFFD700
            )
            return await ctx.send(embed=embed)

        vc.resume()
        title = now_playing.get('title', 'Música Desconhecida')
        embed = discord.Embed(
            title="▶️ Música Retomada",
            description=f"A música **{title}** foi retomada.",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Resume(bot))