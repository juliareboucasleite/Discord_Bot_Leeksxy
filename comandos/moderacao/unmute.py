import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_mute_role(self, guild):
        mute_role = discord.utils.get(guild.roles, name="Silenciado")
        if not mute_role:
            mute_role = discord.utils.get(guild.roles, name="Muted")
        return mute_role

    @commands.command(name='unmute', aliases=['dessilenciar', 'unmutar'], help='Remove o silenciamento de um membro no servidor. Uso: \'unmute <@membro> [motivo]')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute_command(self, ctx, member: discord.Member, *, reason: str = 'Nenhum motivo fornecido.'):
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você não pode se dessilenciar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if member == self.bot.user:
            embed = discord.Embed(
                title="❌ Erro",
                description="Eu não posso ser dessilenciado!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        mute_role = await self.get_mute_role(ctx.guild)
        if not mute_role:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível encontrar o cargo de silenciamento. Certifique-se de que ele foi criado com 'mute.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if mute_role not in member.roles:
            embed = discord.Embed(
                title="ℹ️ Não Silenciado",
                description=f"{member.mention} não está silenciado.",
                color=0xFFCC00
            )
            return await ctx.send(embed=embed)

        try:
            await member.remove_roles(mute_role, reason=reason)
            embed = discord.Embed(
                title="✅ Membro Dessilenciado",
                description=f"{member.mention} foi dessilenciado por {ctx.author.mention}.\n**Motivo:** {reason}",
                color=0xE8E8E8
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)

            # Tentar enviar DM para o membro dessilenciado
            try:
                dm_embed = discord.Embed(
                    title="🔊 Você foi dessilenciado!",
                    description=f"Você foi dessilenciado no servidor **{ctx.guild.name}**.\n**Moderador:** {ctx.author.mention}\n**Motivo:** {reason}",
                    color=0x2ECC71
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                print(f"[WARN] Não foi possível enviar DM para {member.display_name} sobre o dessilenciamento.")

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro de Permissão",
                description="Não tenho permissão para remover o cargo de silenciamento deste membro. Verifique minha hierarquia de cargos e permissões.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar dessilenciar o membro: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Unmute(bot)) 