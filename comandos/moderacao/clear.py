import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', aliases=['limpar', 'purge'], help='Limpa mensagens do canal. Uso: \'clear <quantidade>')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantidade: int = 5):
        await ctx.message.delete()

        if quantidade < 1:
            embed = discord.Embed(
                title="❌ Quantidade Inválida",
                description="Por favor, insira um número positivo de mensagens para apagar.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if quantidade > 100:
            embed = discord.Embed(
                title="⚠️ Limite Excedido",
                description="Não posso apagar mais de 100 mensagens por vez. Definindo para 100.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
            quantidade = 100

        try:
            deleted = await ctx.channel.purge(limit=quantidade)
            
            embed = discord.Embed(
                title="🧹 Limpeza Concluída!",
                description=f"Foram apagadas **{len(deleted)}** mensagens neste canal. (Sua mensagem de comando não está incluída nesta contagem).",
                color=0xE8E8E8
            )
            embed.set_footer(text=f"Comando executado por: {ctx.author.display_name}")
            embed.timestamp = discord.utils.utcnow()
            
            await ctx.send(embed=embed, delete_after=5)

        except discord.Forbidden:
            embed = discord.Embed(
                title="🚫 Permissão Negada",
                description="Não tenho permissão para gerenciar mensagens neste canal. Verifique minhas permissões.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Erro Desconhecido",
                description=f"Ocorreu um erro ao tentar limpar mensagens: `{e}`",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)

    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Permissões Insuficientes",
                description="Você não tem permissão para usar este comando (gerenciar mensagens).",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="❌ Argumento Inválido",
                description="Por favor, insira um número válido de mensagens para apagar.",
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
    await bot.add_cog(Clear(bot))
