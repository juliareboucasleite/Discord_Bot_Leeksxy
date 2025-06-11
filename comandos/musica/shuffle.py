import discord
from discord.ext import commands
import random
from comandos.musica.play import queue
from .utils import now_playing

class Shuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shuffle", aliases=["embaralhar"])
    async def shuffle_command(self, ctx):
        global now_playing
        vc = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Bot Não Conectado",
                description="O bot não está em um canal de voz.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        q = queue.get(ctx.guild.id)

        if not q or len(q) < 2:
            embed = discord.Embed(
                title="❌ Fila Insuficiente",
                description="Não há músicas suficientes na fila para embaralhar (mínimo de 2 músicas).",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        random.shuffle(q)
        
        embed = discord.Embed(
            title="🔀 Fila Embaralhada",
            description="A fila de músicas foi embaralhada com sucesso!",
            color=0xE8E8E8
        )
        
        # Opcional: Mostrar as primeiras músicas da fila embaralhada
        if q:
            shuffled_list = "\n".join([f"• [{song['title']}]({song['url']})" for song in q[:5]])
            embed.add_field(name="Próximas Músicas (embaralhadas)", value=shuffled_list + ("\n..." if len(q) > 5 else ""), inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shuffle(bot))
