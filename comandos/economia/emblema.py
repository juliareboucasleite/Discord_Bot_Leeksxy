import discord
from discord.ext import commands

class Emblema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="emblema",
        description="Mostra um emblema especial.",
        aliases=["badge", "insignia", "medalha", "trofeu", "trophy"],
        help="Mostra seu emblema especial."
    )
    @commands.bot_has_permissions(send_messages=True)
    async def emblema_command(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(
            title="✨ Seu Emblema Especial! ✨",
            description=f"{ctx.author.mention}, você recebeu um emblema por ser um membro incrível do nosso servidor! 🎉",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        # Você pode usar um link de imagem de um emblema genérico ou um GIF divertido aqui
        embed.set_image(url="https://media.giphy.com/media/lMh8fPjXW0X0O/giphy.gif") # Exemplo de gif de um badge/troféu
        embed.set_footer(text="Continue contribuindo para mais conquistas! 🌟")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Emblema(bot))
