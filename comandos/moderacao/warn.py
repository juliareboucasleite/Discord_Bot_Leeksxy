import discord
from discord.ext import commands
import sqlite3

class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='warn', aliases=['avisar', 'advertir'], help='Avisa um membro do servidor. Uso: \'warn <@membro> [motivo]')
    @commands.has_permissions(manage_messages=True) # Permissão comum para moderadores
    @commands.bot_has_permissions(send_messages=True)
    async def warn_command(self, ctx, member: discord.Member, *, reason: str = 'Nenhum motivo fornecido.'):
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Erro",
                description="Você não pode se avisar!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if member == self.bot.user:
            embed = discord.Embed(
                title="❌ Erro",
                description="Eu não posso ser avisado!",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if ctx.author.top_role <= member.top_role and ctx.author.id != ctx.guild.owner_id:
            embed = discord.Embed(
                title="❌ Permissões Insuficientes",
                description="Você não pode avisar este membro porque o cargo dele é igual ou superior ao seu.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO warnings (user_id, guild_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                           (member.id, ctx.guild.id, ctx.author.id, reason))
            conn.commit()

            embed = discord.Embed(
                title="✅ Membro Avisado",
                description=f"{member.mention} foi avisado por {ctx.author.mention}.\n**Motivo:** {reason}",
                color=0xE8E8E8
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)

            # Tentar enviar DM para o membro avisado
            try:
                dm_embed = discord.Embed(
                    title="⚠️ Você recebeu um aviso!",
                    description=f"Você recebeu um aviso no servidor **{ctx.guild.name}**.\n**Moderador:** {ctx.author.mention}\n**Motivo:** {reason}",
                    color=0xFFCC00
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                print(f"[WARN] Não foi possível enviar DM para {member.display_name} sobre o aviso.")

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar avisar o membro: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Warn(bot)) 