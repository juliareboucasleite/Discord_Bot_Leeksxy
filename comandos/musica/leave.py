import discord
from discord.ext import commands
from .utils import now_playing

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leave", aliases=["sair", "desconectar"])
    async def leave_command(self, ctx):
        if not ctx.guild.voice_client:
            return await ctx.send("❌ Eu não estou em um canal de voz.")

        embed = discord.Embed(
            title="👋 Saindo do Canal de Voz",
            description=f"Desconectado do canal de voz **{ctx.guild.voice_client.channel.name}**.",
            color=0xE8E8E8
        )
        await ctx.guild.voice_client.disconnect()
        
        # Limpar now_playing quando o bot sair do canal de voz
        global now_playing
        now_playing = {'title': 'Nenhuma música tocando', 'url': None, 'requester': None}

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leave(bot))
