import discord
from discord.ext import commands
import random

class Fato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fato', aliases=['fact'], help='Obtém um fato aleatório.')
    @commands.bot_has_permissions(send_messages=True)
    async def fato_command(self, ctx):
        fatos = [
            "O mel nunca estraga. Arqueólogos encontraram potes de mel em tumbas egípcias que ainda eram comestíveis.",
            "Um polvo tem três corações.",
            "O olho de uma avestruz é maior do que o seu cérebro.",
            "As abelhas conseguem voar mais alto que o Monte Everest.",
            "A Estátua da Liberdade foi um presente da França para os Estados Unidos.",
            "Os pandas gigantes comem bambu por cerca de 12 horas por dia.",
            "Os cavalos e os ratos não vomitam.",
            "As formigas podem levantar 50 vezes o seu próprio peso.",
            "Um caracol pode dormir por três anos.",
            "O som que um camelo faz é chamado de 'grunhido'.",
            "Os flamingos comem de cabeça para baixo.",
            "O DNA de um chimpanzé é 98% idêntico ao de um humano.",
            "Um raio é mais quente do que a superfície do sol.",
            "Os ursos polares têm pele preta por baixo de seu pelo branco.",
            "Os gatos podem fazer mais de 100 sons diferentes, enquanto os cães podem fazer apenas cerca de 10."
        ]
        
        fato = random.choice(fatos)
        
        embed = discord.Embed(
            title="💡 Fato Aleatório",
            description=fato,
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fato(bot)) 