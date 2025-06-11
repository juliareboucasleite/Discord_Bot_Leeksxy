import discord
from discord.ext import commands
import sqlite3
import random
from datetime import datetime, timedelta

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='work', aliases=['trabalhar', 'trabalho', 'job'], help='Trabalhe e ganhe moedas. Uso: \'work')
    @commands.bot_has_permissions(send_messages=True)
    async def work_command(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        min_reward = 100
        max_reward = 300
        cooldown_hours = 4 # Cooldown de 4 horas

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT balance, last_work FROM user_economy WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
            result = cursor.fetchone()

            if result:
                balance, last_work_str = result
                if last_work_str:
                    last_work = datetime.fromisoformat(last_work_str)
                    time_since_last_work = datetime.utcnow() - last_work
                    if time_since_last_work < timedelta(hours=cooldown_hours):
                        remaining_time = timedelta(hours=cooldown_hours) - time_since_last_work
                        hours, remainder = divmod(int(remaining_time.total_seconds()), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        embed = discord.Embed(
                            title="⏰ Cooldown",
                            description=f"Você já trabalhou recentemente! Volte em {hours}h {minutes}m {seconds}s.",
                            color=0xFFCC00
                        )
                        return await ctx.send(embed=embed)

                reward_amount = random.randint(min_reward, max_reward)
                cursor.execute("UPDATE user_economy SET balance = ?, last_work = ? WHERE user_id = ? AND guild_id = ?",
                               (balance + reward_amount, datetime.utcnow().isoformat(), user_id, guild_id))
            else:
                # Cria uma nova entrada para o usuário
                reward_amount = random.randint(min_reward, max_reward)
                cursor.execute("INSERT INTO user_economy (user_id, guild_id, balance, last_work) VALUES (?, ?, ?, ?)",
                               (user_id, guild_id, reward_amount, datetime.utcnow().isoformat()))
            conn.commit()

            embed = discord.Embed(
                title="💼 Trabalho Concluído!",
                description=f"Você trabalhou e ganhou **{reward_amount} moedas**! Seu saldo atual é de **{balance + reward_amount if result else reward_amount} moedas**.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="❌ Erro",
                description=f"Ocorreu um erro ao tentar trabalhar: {e}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(Work(bot)) 