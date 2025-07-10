import discord
from discord.ext import commands
from .utils import looping

class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="loop", aliases=["repetir", "repetir_musica"])
    async def loop_command(self, ctx):
        if not ctx.guild.voice_client:
            await ctx.send("❌ O bot não está em um canal de voz.", ephemeral=True)
            return

        if not ctx.guild.voice_client.is_playing() and not ctx.guild.voice_client.is_paused():
            await ctx.send("❌ Não há música tocando para colocar em loop.", ephemeral=True)
            return

        # Inverte o estado do loop para o servidor atual
        looping[ctx.guild.id] = not looping.get(ctx.guild.id, False)
        
        if looping.get(ctx.guild.id):
            embed = discord.Embed(
                title="🔁 Loop Ativado",
                description="A música atual será repetida indefinidamente.",
                color=0xE8E8E8
            )
        else:
            embed = discord.Embed(
                title="▶️ Loop Desativado",
                description="A música não será mais repetida.",
                color=0xE8E8E8
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Loop(bot))
