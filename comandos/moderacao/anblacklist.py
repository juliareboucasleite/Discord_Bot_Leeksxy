import discord
from discord.ext import commands
import sqlite3
from typing import Optional
import os

OWNER_IDS = os.getenv("CRIADORA_ID", "").split(",")

class AnBlacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='anblacklist', help='Remove um usuário da blacklist. Uso: anblacklist <@usuário>')
    async def anblacklist(self, ctx, user: Optional[discord.User] = None):
        if str(ctx.author.id) not in OWNER_IDS:
            return await ctx.send('Comando apenas para devs!')

        if not user:
            return await ctx.send('Mencione um usuário!')

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM blacklist WHERE user_id = ?', (user.id,))
            result = cursor.fetchone()
            if not result:
                return await ctx.send('Esse usuário não está na blacklist!')
            cursor.execute('DELETE FROM blacklist WHERE user_id = ?', (user.id,))
            conn.commit()
            await ctx.send('Retirei ele da blacklist!')
            print(f"[BLACKLIST] Usuário {user} removido da blacklist por {ctx.author}")
        except Exception as e:
            await ctx.send(f'Erro ao remover da blacklist: {e}')
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(AnBlacklist(bot))