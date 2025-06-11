import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="say",
        description="Faz o bot repetir uma mensagem.",
        aliases=["falar", "dizer", "speak", "fala", "diz"]
    )
    async def say(self, ctx, *, mensagem: str = None):
        await ctx.message.delete()

        if not mensagem:
            embed = discord.Embed(
                title="🤔 O que devo dizer?",
                description="Por favor, me diga o que você quer que eu fale.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="🗣️ Mensagem Enviada!",
            description=f"Você me pediu para dizer:\n\n>>> {mensagem}",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        embed.set_footer(text=f"Mensagem enviada por: {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @say.error
    async def say_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Argumento Ausente",
                description="Você precisa fornecer uma mensagem para eu repetir.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="⚠️ Erro Desconhecido",
                description=f"Ocorreu um erro: `{error}`",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Say(bot))
