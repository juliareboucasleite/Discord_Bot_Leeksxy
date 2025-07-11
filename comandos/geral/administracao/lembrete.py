import discord
from discord.ext import commands
import asyncio
import re

class Lembrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lembrar")
    async def lembrar(self, ctx, tempo=None, *, mensagem=None):
        if not tempo:
            return await ctx.send("⏰ Defina um tempo! (ex: `10s`, `5m`, `2h`, `1d`)")
        if not mensagem:
            return await ctx.send("📝 Insira a mensagem que devo lembrar você!")

        # Regex para capturar tempo e unidade
        match = re.match(r"^(\d+)([smhd])$", tempo.lower())
        if not match:
            return await ctx.send("❌ Formato inválido. Use por exemplo `10s`, `2m`, `1h`, `1d`")

        valor, unidade = int(match[1]), match[2]

        # Converter para segundos
        multiplicadores = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        segundos = valor * multiplicadores[unidade]

        await ctx.send(f"⏳ Ok {ctx.author.mention}, vou te lembrar de `{mensagem}` daqui `{valor}{unidade}`.")

        await asyncio.sleep(segundos)
        await ctx.send(f"🔔 {ctx.author.mention}, lembrete: **{mensagem}**")

def setup(bot):
    bot.add_cog(Lembrar(bot))
