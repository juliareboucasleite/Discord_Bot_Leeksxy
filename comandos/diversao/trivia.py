import discord
from discord.ext import commands
import random

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {
                "title": "Nome do meu criador",
                "options": ["Duda", "Mady", "Julia", "Madeleine"],
                "correct": 3
            },
            {
                "title": "Jogo favorito do meu criador",
                "options": ["Lol", "Valorant", "Delta", "Gta V", "Roblox"],
                "correct": 2
            },
            {
                "title": "Anime Favorito do meu criador",
                "options": ["darlling trefranquis", "Naruto", "Violet Evergarden", "Boruto"],
                "correct": 3
            },
            {
                "title": "29+29+29+29+29-100",
                "options": ["145", "125", "45", "100"],
                "correct": 3
            },
            {
                "title": "Em que ano aconteceu a peste negra?",
                "options": ["1346 – 1353", "1245 - 1259", "1059 - 1256", "1346 - 1359"],
                "correct": 1
            }
        ]

    @commands.command(name="trivia")
    async def trivia(self, ctx):
        q = random.choice(self.questions)
        options = ""
        for i, opt in enumerate(q["options"], 1):
            options += f"{i} - {opt}\n"

        embed = discord.Embed(
            title=q["title"],
            description=options,
            color=discord.Color.green()
        )
        embed.set_footer(text="Responda com o número correto! Você tem 15 segundos.")

        await ctx.send(embed=embed)

        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
            if int(msg.content.strip()) == q["correct"]:
                await ctx.send("✅ Você acertou!")
            else:
                await ctx.send("❌ Você errou a resposta.")
        except:
            await ctx.send("⏰ Você não respondeu a tempo!")

def setup(bot):
    bot.add_cog(Trivia(bot))
