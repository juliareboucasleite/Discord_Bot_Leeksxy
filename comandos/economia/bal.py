import discord
from discord.ext import commands
import sqlite3

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='bal', aliases=[], help='Verifica seu saldo de moedas ou o de outro membro. Uso: \'bal [@membro]')
    @commands.bot_has_permissions(send_messages=True)
    async def balance_command(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user_id = member.id
        guild_id = ctx.guild.id

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance FROM user_economy WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
            result = cursor.fetchone()

            balance = result[0] if result else 0
            
            if member == ctx.author:
                embed = discord.Embed(
                    title="💰 Seu Saldo",
                    description=f"Você tem **{balance} moedas**.",
                    color=0xE8E8E8
                )
            else:
                embed = discord.Embed(
                    title="💰 Saldo do Membro",
                    description=f"{member.mention} tem **{balance} moedas**.",
                    color=0xE8E8E8
                )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao verificar o saldo: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Balance(bot)) 