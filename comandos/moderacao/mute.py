import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_mute_role(self, guild):
        # Tenta encontrar o cargo "Silenciado" ou "Muted"
        mute_role = discord.utils.get(guild.roles, name="Silenciado")
        if not mute_role:
            mute_role = discord.utils.get(guild.roles, name="Muted")
        
        if not mute_role:
            # Se o cargo não existe, cria-o e configura as permissões
            try:
                mute_role = await guild.create_role(name="Silenciado", reason="Cargo para silenciar membros.", color=0x747F8D) # Cor cinza Discord
                for channel in guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False, speak=False)
                print(f"[INFO] Cargo 'Silenciado' criado e permissões configuradas no servidor {guild.name}.")
            except discord.Forbidden:
                print(f"[ERROR] Permissões insuficientes para criar o cargo 'Silenciado' no servidor {guild.name}.")
                return None
            except Exception as e:
                print(f"[ERROR] Erro ao criar ou configurar cargo 'Silenciado' no servidor {guild.name}: {e}")
                return None
        return mute_role

    @commands.command(name='mute', aliases=['silenciar', 'mutar'], help='Silencia um membro no servidor. Uso: \'mute <@membro> [motivo]')
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True, manage_channels=True)
    async def mute_command(self, ctx, member: discord.Member, *, reason: str = 'Nenhum motivo fornecido.'):
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você não pode se silenciar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if member == self.bot.user:
            embed = discord.Embed(
                title="❌ Erro",
                description="Eu não posso me silenciar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes",
                description="Você não pode silenciar este membro porque o cargo dele é igual ou superior ao seu.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if ctx.guild.me.top_role <= member.top_role:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes do Bot",
                description="Não consigo silenciar este membro porque o cargo dele é igual ou superior ao meu.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        mute_role = await self.get_mute_role(ctx.guild)
        if not mute_role:
            embed = discord.Embed(
                title="❌ Erro",
                description="Não foi possível obter ou criar o cargo de silenciamento. Verifique as permissões do bot.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if mute_role in member.roles:
            embed = discord.Embed(
                title="ℹ️ Já Silenciado",
                description=f"{member.mention} já está silenciado.",
                color=0xFFCC00
            )
            return await ctx.send(embed=embed)

        try:
            await member.add_roles(mute_role, reason=reason)
            embed = discord.Embed(
                title="✅ Membro Silenciado",
                description=f"{member.mention} foi silenciado por {ctx.author.mention}.\n**Motivo:** {reason}",
                color=0xE8E8E8
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)

            # Tentar enviar DM para o membro silenciado
            try:
                dm_embed = discord.Embed(
                    title="🔇 Você foi silenciado!",
                    description=f"Você foi silenciado no servidor **{ctx.guild.name}**.\n**Moderador:** {ctx.author.mention}\n**Motivo:** {reason}",
                    color=0xFFCC00
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                print(f"[WARN] Não foi possível enviar DM para {member.display_name} sobre o silenciamento.")

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Erro de Permissão",
                description="Não tenho permissão para adicionar o cargo de silenciamento a este membro. Verifique minha hierarquia de cargos e permissões.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar silenciar o membro: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mute(bot)) 