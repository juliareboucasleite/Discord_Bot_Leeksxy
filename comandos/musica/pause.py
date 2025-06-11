import discord
from discord.ext import commands
from .utils import now_playing

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pause", aliases=["pausar"])
    async def pause_command(self, ctx):
        global now_playing
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(
                title="❌ Nada Tocando",
                description="Não há nenhuma música tocando no momento para pausar.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if vc.is_paused():
            embed = discord.Embed(
                title="⚠️ Já Pausado",
                description="A música já está pausada.",
                color=0xFFD700
            )
            return await ctx.send(embed=embed)

        vc.pause()
        title = now_playing.get('title', 'Música Desconhecida')
        embed = discord.Embed(
            title="⏸️ Música Pausada",
            description=f"A música **{title}** foi pausada.",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Pause(bot))