import discord
from discord.ext import commands
from .utils import now_playing
from utils.progressBar import progress_bar

class NowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nowplaying", aliases=["np", "tocando_agora"])
    async def now_playing_command(self, ctx):
        if not ctx.guild.voice_client or not ctx.guild.voice_client.is_playing():
            embed = discord.Embed(
                title="🎶 Nenhuma Música Tocando",
                description="Não há nenhuma música tocando no momento.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed)

        # Acessa as informações da música tocando para este servidor
        current_song_info = now_playing.get(ctx.guild.id, {})

        title = current_song_info.get('title')
        url = current_song_info.get('url')
        requester = current_song_info.get('requester')
        duration = current_song_info.get('duration')
        thumbnail = current_song_info.get('thumbnail')

        if not title or not url:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível obter as informações da música atual.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        # Tenta obter o tempo atual da música
        tempo_atual = None
        if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
            try:
                tempo_atual = int(ctx.guild.voice_client.source.seek() if hasattr(ctx.guild.voice_client.source, 'seek') else ctx.guild.voice_client.source._player._position // 1000)
            except Exception:
                tempo_atual = None
        if tempo_atual is None:
            tempo_atual = 0

        # Barra de progresso
        barra = ""
        porcentagem = ""
        if duration and duration > 0:
            pb = progress_bar(tempo_atual, duration, 20)
            barra = pb["bar"]
            porcentagem = pb["percentage_text"]

        embed = discord.Embed(
            title="💿 Tocando Agora",
            description=f"[{title}]({url})",
            color=0xE8E8E8
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Pedida por", value=requester if requester else "Desconhecido", inline=True)
        if duration and duration > 0:
            embed.add_field(
                name="Progresso",
                value=f"{barra} `{porcentagem}`\n{tempo_atual}s / {duration}s",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NowPlaying(bot))
