from discord.ext import commands
import time

inicio = time.time()

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status", aliases=["uptime", "online"], help="Mostra o tempo de atividade do bot.")
    async def status(self, ctx):
        atual = time.time()
        uptime = atual - inicio
        minutos, segundos = divmod(int(uptime), 60)
        horas, minutos = divmod(minutos, 60)
        await ctx.send(f"🕒 Online há {horas}h {minutos}min {segundos}s")

async def setup(bot):
    await bot.add_cog(Status(bot))
