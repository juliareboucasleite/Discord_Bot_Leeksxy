import discord
from discord.ext import commands
from comandos.musica.play import queue
from .utils import now_playing, looping


class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skip", aliases=["pular"])
    async def skip_command(self, ctx):
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
                description="Não há nenhuma música tocando para pular.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        # Para a música atual para acionar o 'after' callback
        vc.stop()

        embed = discord.Embed(
            title="⏭️ Música Pulada",
            description="Pulando para a próxima música na fila...",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Skip(bot))
