import discord
from discord.ext import commands
import random

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", aliases=["jogarmoeda"])
    async def coinflip(self, ctx, escolha=None):
        opcoes = ['cara', 'coroa']
        resultado = random.choice(opcoes)

        if escolha is None or escolha.lower() not in opcoes:
            await ctx.reply("Insira **cara** ou **coroa** depois do comando.")
            return

        if escolha.lower() == resultado:
            await ctx.send(f"Deu **{resultado}**, você ganhou dessa vez.")
        else:
            await ctx.send(f"Deu **{resultado}**, você perdeu dessa vez.")

def setup(bot):
    bot.add_cog(CoinFlip(bot))
