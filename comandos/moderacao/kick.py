import discord
from discord.ext import commands
from typing import Optional

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', aliases=['expulsar', 'kickar'], help="Expulsa um membro do servidor. Uso: 'kick <@membro> [motivo]")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: Optional[discord.Member], *, reason: str = 'Nenhum motivo fornecido.'):
        try:
            await ctx.message.delete()
        except Exception:
            pass  # Ignora se não conseguir deletar a mensagem

        COR_SUCESSO = 0x43B581
        COR_ERRO = 0xFF0000
        COR_AVISO = 0xFFCC00

        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você não pode se expulsar!",
                color=COR_ERRO
            )
            return await ctx.send(embed=embed)

        if member == self.bot.user:
            embed = discord.Embed(
                title="❌ Erro",
                description="Eu não posso me expulsar!",
                color=COR_AVISO
            )
            return await ctx.send(embed=embed)

        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes",
                description="Você não pode expulsar este membro porque o cargo dele é igual ou superior ao seu.",
                color=COR_AVISO
            )
            return await ctx.send(embed=embed)

        if ctx.guild.me.top_role <= member.top_role:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes do Bot",
                description="Não consigo expulsar este membro porque o cargo dele é igual ou superior ao meu.",
                color=COR_ERRO
            )
            return await ctx.send(embed=embed)
        
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Expulso",
                description=f"{member.mention} foi expulso do servidor.\n**Motivo:** {reason}",
                color=COR_SUCESSO
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)
            print(f"[KICK] {member} expulso por {ctx.author} no servidor {ctx.guild.name} (Motivo: {reason})")
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro de Permissão",
                description="Não tenho permissão para expulsar este membro. Verifique minha hierarquia de cargos e permissões.",
                color=COR_ERRO
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar expulsar o membro: {e}",
                color=COR_ERRO
            )
            await ctx.send(embed=embed)
            print(f"[ERRO KICK] {e}")

async def setup(bot):
    await bot.add_cog(Kick(bot)) 