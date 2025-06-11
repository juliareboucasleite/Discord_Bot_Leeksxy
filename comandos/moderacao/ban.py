import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban', aliases=['banir'], help='Bane um membro do servidor. Uso: \'ban <@membro> [motivo]')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membro: discord.Member = None, *, motivo="Sem motivo"):
        await ctx.message.delete()

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem banir?",
                description="Por favor, mencione um membro para banir.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="❌ Você não pode se banir!",
                description="Você não pode banir a si mesmo do servidor.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)
        
        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="🚫 Eu não posso me banir!",
                description="Você tentou me banir? Isso não é legal!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
            embed = discord.Embed(
                title="⚠️ Permissões Insuficientes",
                description="Você não tem permissão para banir este membro, pois o cargo dele é igual ou superior ao seu.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.top_role >= ctx.guild.me.top_role:
            embed = discord.Embed(
                title="⚠️ Permissões do Bot Insuficientes",
                description="Não tenho permissão para banir este membro, pois o cargo dele é igual ou superior ao meu.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        try:
            await membro.ban(reason=motivo)
            embed = discord.Embed(
                title="🔨 Membro Banido!",
                description=f"**{membro.display_name}** foi banido(a) por **{ctx.author.display_name}**.",
                color=0xE8E8E8
            )
            embed.add_field(name="Usuário", value=f"{membro.mention} (ID: {membro.id})", inline=False)
            embed.add_field(name="Moderador", value=f"{ctx.author.mention} (ID: {ctx.author.id})", inline=False)
            embed.add_field(name="Motivo", value=motivo, inline=False)
            embed.set_thumbnail(url=membro.avatar.url if membro.avatar else None)
            embed.set_footer(text=f"Banido em: {discord.utils.utcnow().strftime('%d/%m/%Y %H:%M')}")
            embed.timestamp = discord.utils.utcnow()
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="🚫 Permissão Negada",
                description="Não tenho permissão para banir este membro. Por favor, verifique minhas permissões.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Erro ao Banir",
                description=f"Ocorreu um erro inesperado ao tentar banir o membro: `{e}`",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)

    @ban.error
    async def ban_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="❌ Argumento Ausente",
                description="Você precisa mencionar o membro que deseja banir.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Permissões Insuficientes",
                description="Você não tem permissão para usar este comando (ban_members).",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title="❌ Membro Não Encontrado",
                description="Não consegui encontrar o membro que você mencionou.",
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
    await bot.add_cog(Ban(bot))
