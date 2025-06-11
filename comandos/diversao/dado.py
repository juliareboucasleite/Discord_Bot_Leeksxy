import discord
from discord.ext import commands
import random

class Dado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dado', aliases=['dice', 'rolardado', 'roll'], help='Joga um dado de 6 lados. Uso: \'dado')
    @commands.bot_has_permissions(send_messages=True)
    async def dado_command(self, ctx):
        resultado = random.randint(1, 6)
        embed = discord.Embed(
            title="🎲 Jogada de Dado",
            description=f"Você rolou o dado e o resultado foi: **{resultado}**!",
            color=0xE8E8E8
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1070/1070564.png") # Ícone de dado
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Dado(bot)) 