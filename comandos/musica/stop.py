import discord
from discord.ext import commands
from comandos.musica.play import queue
from .utils import now_playing, looping


class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop", aliases=["parar", "desativar"])
    async def stop_command(self, ctx):
        global now_playing, looping
        vc = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Bot Não Conectado",
                description="O bot não está em um canal de voz.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if not vc.is_playing() and not vc.is_paused():
            embed = discord.Embed(
                title="❌ Nada Tocando",
                description="Não há nenhuma música tocando ou pausada para parar.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        vc.stop()
        queue[ctx.guild.id] = []  # Limpa a fila
        now_playing = {'title': 'Nenhuma música tocando', 'url': None, 'requester': None}
        looping = False

        embed = discord.Embed(
            title="⏹️ Reprodução Parada",
            description="A reprodução da música foi parada e a fila foi limpa.",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Stop(bot))
