import discord
from discord.ext import commands
import sqlite3

class Unwarn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='unwarn', aliases=['desavisar', 'removewarn', 'removeraviso'], help='Remove um aviso de um membro. Uso: \'unwarn <ID_do_aviso>')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(send_messages=True)
    async def unwarn_command(self, ctx, warning_id: int):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM warnings WHERE id = ? AND guild_id = ?", (warning_id, ctx.guild.id))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                cursor.execute("DELETE FROM warnings WHERE id = ? AND guild_id = ?", (warning_id, ctx.guild.id))
                conn.commit()

                member = ctx.guild.get_member(user_id) # Tentar obter o objeto membro
                member_mention = member.mention if member else f"Membro (ID: {user_id})"

                embed = discord.Embed(
                    title="✅ Aviso Removido",
                    description=f"O aviso com ID `{warning_id}` de {member_mention} foi removido por {ctx.author.mention}.",
                    color=0xE8E8E8
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="❌ Aviso Não Encontrado",
                    description=f"Nenhum aviso com o ID `{warning_id}` foi encontrado para este servidor.",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar remover o aviso: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Unwarn(bot)) 