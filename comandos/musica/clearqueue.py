import discord
from discord.ext import commands
from comandos.musica.play import queue

class ClearQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clearqueue", aliases=["limparfila", "cq"])
    async def clear_queue_command(self, ctx):
        if not ctx.guild.voice_client:
            return await ctx.send("❌ Não estou em um canal de voz.")

        if ctx.guild.id not in queue or not queue[ctx.guild.id]:
            return await ctx.send("❌ A fila já está vazia.")

        # Limpa a fila
        queue[ctx.guild.id] = []
        
        embed = discord.Embed(
            title="🗑️ Fila Limpa",
            description="A fila de músicas foi limpa com sucesso!",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ClearQueue(bot))
