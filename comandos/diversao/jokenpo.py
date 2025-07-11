import discord
from discord.ext import commands
import random

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps")
    async def rps(self, ctx, escolha=None):
        opcoes = ['pedra', 'papel', 'tesoura']

        if not escolha or escolha.lower().strip() not in opcoes:
            await ctx.reply("Escolha `pedra`, `papel` ou `tesoura`.")
            return

        escolha = escolha.lower().strip()
        bot_escolha = random.choice(opcoes)

        msg = f"Você escolheu `{escolha}` e eu escolhi `{bot_escolha}`, "
        if escolha == bot_escolha:
            resultado = "deu empate!"
        elif (
            (escolha == "tesoura" and bot_escolha == "papel") or
            (escolha == "papel" and bot_escolha == "pedra") or
            (escolha == "pedra" and bot_escolha == "tesoura")
        ):
            resultado = "você ganhou!"
        else:
            resultado = "eu ganhei!"

        await ctx.reply(msg + resultado)

def setup(bot):
    bot.add_cog(RPS(bot))
