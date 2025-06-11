import discord
from discord.ext import commands
from .utils import now_playing

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

        if not title or not url:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível obter as informações da música atual.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="💿 Tocando Agora",
            description=f"[{title}]({url})",
            color=0xE8E8E8
        )
        # Se houver um thumbnail disponível, você pode adicioná-lo aqui
        # embed.set_thumbnail(url=current_song_info.get('thumbnail'))
        embed.add_field(name="Pedida por", value=requester if requester else "Desconhecido", inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NowPlaying(bot))
