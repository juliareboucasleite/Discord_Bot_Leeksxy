import discord
from discord.ext import commands
import random

class Moeda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='moeda', aliases=['coin', 'caraoucoroa', 'flip', 'coinflip'], help='Joga uma moeda: cara ou coroa. Uso: \'moeda')
    @commands.bot_has_permissions(send_messages=True)
    async def moeda_command(self, ctx):
        opcoes = ["Cara", "Coroa"]
        resultado = random.choice(opcoes)
        
        emoji = "⚪" # Emoji padrão
        if resultado == "Cara":
            emoji = "😀"
        else:
            emoji = "👑"

        embed = discord.Embed(
            title="🪙 Jogada de Moeda",
            description=f"Você jogou a moeda e caiu: **{resultado}** {emoji}!",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moeda(bot)) 