import discord
from discord.ext import commands
import openai
import os

class Pergunta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @commands.command(name="pergunta", aliases=["chatgpt", "ia"], help="Pergunte qualquer coisa para a IA!")
    async def pergunta(self, ctx, *, pergunta: str):
        await ctx.trigger_typing()
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente útil e responde em português."},
                    {"role": "user", "content": pergunta}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            resposta = response.choices[0].message.content.strip()
            await ctx.send(f"🤖 {resposta}")
        except Exception as e:
            await ctx.send(f"❌ Erro ao consultar a IA: {e}")

async def setup(bot):
    await bot.add_cog(Pergunta(bot))