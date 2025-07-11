import discord
from discord.ext import commands
import asyncio
import re
from typing import Optional

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='timer', aliases=['cronometro', 'temporizador'], help='Define um timer. Uso: timer <tempo> (ex: 10m, 1h, 2d)')
    async def timer(self, ctx, tempo: Optional[str] = None):
        if not tempo:
            return await ctx.send('Fale o tempo do seu timer!')
        match = re.match(r'^(\d+)([mhd])$', tempo)
        if not match:
            return await ctx.send('Formato inválido! Use m para minutos, h para horas e d para dias. Exemplo: 10m, 1h, 2d')
        valor, unidade = int(match.group(1)), match.group(2)
        segundos = valor * 60 if unidade == 'm' else valor * 3600 if unidade == 'h' else valor * 86400
        await ctx.reply(f'Irei te chamar em {tempo}, aguarde alguns segundos...')
        await asyncio.sleep(segundos)
        await ctx.reply(f'Seu tempo de {tempo} acabou, volte mais tarde!')

async def setup(bot):
    await bot.add_cog(Timer(bot))