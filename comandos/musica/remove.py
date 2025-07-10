import discord
from discord.ext import commands
from comandos.musica.play import queue
from .utils import now_playing

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remove", aliases=["remover"])
    async def remove_command(self, ctx, index: int):
        vc = ctx.voice_client

        if not vc:
            embed = discord.Embed(
                title="❌ Bot Não Conectado",
                description="O bot não está em um canal de voz.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        q = queue.get(ctx.guild.id)

        if not q:
            embed = discord.Embed(
                title="❌ Fila Vazia",
                description="A fila de músicas está vazia.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if not (1 <= index <= len(q)):
            embed = discord.Embed(
                title="⚠️ Índice Inválido",
                description=f"Por favor, forneça um número de 1 a {len(q)}.",
                color=0xFFD700
            )
            return await ctx.send(embed=embed)

        removed_song = q.pop(index - 1)
        
        embed = discord.Embed(
            title="🗑️ Música Removida",
            description=f"A música **[{removed_song['title']}]({removed_song['url']})** foi removida da fila.",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Remove(bot)) 