import discord
from discord.ext import commands
import random

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball', aliases=['magic8ball', 'bolamagica'], help='Pergunta à Bola 8 Mágica. Uso: \'8ball <sua pergunta>')
    @commands.bot_has_permissions(send_messages=True)
    async def eightball_command(self, ctx, *, pergunta: str):
        respostas = [
            "Sim, definitivamente.",
            "É certo.",
            "Sem dúvida.",
            "Com certeza.",
            "Você pode contar com isso.",
            "A meu ver, sim.",
            "Provavelmente.",
            "Perspectiva boa.",
            "Sim.",
            "Sinais apontam que sim.",
            "Resposta nebulosa, tente novamente.",
            "Pergunte novamente mais tarde.",
            "Melhor não te dizer agora.",
            "Não é possível prever agora.",
            "Concentre-se e pergunte novamente.",
            "Não conte com isso.",
            "Minha resposta é não.",
            "Minhas fontes dizem que não.",
            "Perspectiva não tão boa.",
            "Muito duvidoso."
        ]
        
        resposta = random.choice(respostas)
        
        embed = discord.Embed(
            title="🎱 Bola 8 Mágica",
            color=0xE8E8E8
        )
        embed.add_field(name="🤔 Sua Pergunta:", value=pergunta, inline=False)
        embed.add_field(name="🔮 Minha Resposta:", value=resposta, inline=False)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Eight_ball_icon.svg/1200px-Eight_ball_icon.svg.png")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EightBall(bot)) 