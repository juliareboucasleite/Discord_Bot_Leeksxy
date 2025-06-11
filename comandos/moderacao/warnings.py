import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='warnings', aliases=['warns', 'avisos', 'veravisos', 'listwarnings'], help='Exibe todos os avisos de um membro. Uso: \'warnings <@membro>')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def warnings_command(self, ctx, member: discord.Member):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, moderator_id, reason, timestamp FROM warnings WHERE user_id = ? AND guild_id = ? ORDER BY timestamp DESC",
                           (member.id, ctx.guild.id))
            results = cursor.fetchall()

            if not results:
                embed = discord.Embed(
                    title="ℹ️ Nenhum Aviso Encontrado",
                    description=f"{member.mention} não possui avisos neste servidor.",
                    color=0xE8E8E8
                )
                await ctx.send(embed=embed)
                return

            description = f"**Avisos para {member.mention}:**\n\n"
            for warn_id, moderator_id, reason, timestamp_str in results:
                moderator = ctx.guild.get_member(moderator_id)
                moderator_mention = moderator.mention if moderator else f"Moderador (ID: {moderator_id})"
                
                # Formatar a data e hora para um formato mais legível
                try:
                    dt_object = datetime.fromisoformat(timestamp_str)
                    formatted_time = dt_object.strftime("%d/%m/%Y %H:%M:%S")
                except ValueError:
                    formatted_time = timestamp_str # Fallback se o formato não for ISO

                description += (
                    f"**ID do Aviso:** `{warn_id}`\n"
                    f"**Motivo:** {reason}\n"
                    f"**Moderador:** {moderator_mention}\n"
                    f"**Data/Hora:** {formatted_time} UTC\n"
                    f"---\n"
                )
            
            embed = discord.Embed(
                title=f"📋 Avisos de {member.display_name}",
                description=description,
                color=0xE8E8E8
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar buscar os avisos: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Warnings(bot)) 