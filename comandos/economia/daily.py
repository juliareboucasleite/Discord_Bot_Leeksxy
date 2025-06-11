import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='daily', aliases=['diario', 'recompensa', 'reward'], help='Colete sua recompensa diária de moedas.')
    @commands.bot_has_permissions(send_messages=True)
    async def daily_command(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        reward_amount = 500 # Quantidade de moedas diárias

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance, last_daily FROM user_economy WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
            result = cursor.fetchone()

            if result:
                balance, last_daily_str = result
                if last_daily_str:
                    last_daily = datetime.fromisoformat(last_daily_str)
                    time_since_last_daily = datetime.utcnow() - last_daily
                    if time_since_last_daily < timedelta(days=1):
                        remaining_time = timedelta(days=1) - time_since_last_daily
                        hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        embed = discord.Embed(
                            title="⏰ Recompensa Diária",
                            description=f"Você já coletou sua recompensa diária! Volte em {hours}h {minutes}m {seconds}s.",
                            color=0xFFCC00
                        )
                        return await ctx.send(embed=embed)

                # Atualiza o saldo e a data do último daily
                cursor.execute("UPDATE user_economy SET balance = ?, last_daily = ? WHERE user_id = ? AND guild_id = ?",
                               (balance + reward_amount, datetime.utcnow().isoformat(), user_id, guild_id))
            else:
                # Cria uma nova entrada para o usuário
                cursor.execute("INSERT INTO user_economy (user_id, guild_id, balance, last_daily) VALUES (?, ?, ?, ?)",
                               (user_id, guild_id, reward_amount, datetime.utcnow().isoformat()))
            conn.commit()

            embed = discord.Embed(
                title="💰 Recompensa Diária Coletada!",
                description=f"Você coletou **{reward_amount} moedas**! Seu saldo atual é de **{balance + reward_amount if result else reward_amount} moedas**.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao coletar a recompensa diária: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Daily(bot)) 