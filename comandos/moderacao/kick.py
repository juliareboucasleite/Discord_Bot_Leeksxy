import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', aliases=['expulsar', 'kickar'], help='Expulsa um membro do servidor. Uso: \'kick <@membro> [motivo]')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member, *, reason: str = 'Nenhum motivo fornecido.'):
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você não pode se expulsar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if member == self.bot.user:
            embed = discord.Embed(
                title="❌ Erro",
                description="Eu não posso me expulsar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes",
                description="Você não pode expulsar este membro porque o cargo dele é igual ou superior ao seu.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if ctx.guild.me.top_role <= member.top_role:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes do Bot",
                description="Não consigo expulsar este membro porque o cargo dele é igual ou superior ao meu.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)
        
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Membro Expulso",
                description=f"{member.mention} foi expulso do servidor.\n**Motivo:** {reason}",
                color=0xE8E8E8
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro de Permissão",
                description="Não tenho permissão para expulsar este membro. Verifique minha hierarquia de cargos e permissões.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar expulsar o membro: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Kick(bot)) 