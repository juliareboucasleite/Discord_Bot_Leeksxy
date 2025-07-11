import discord
from discord.ext import commands
import sqlite3

class DelSugestao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='delsugestao', help='Remove o canal de sugestões configurado.')
    @commands.has_permissions(administrator=True)
    async def delsugestao(self, ctx):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT sugestao_channel_id FROM guild_settings WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            await ctx.send('O canal de sugestões nem foi setado! Como você quer que eu retire o canal?')
            conn.close()
            return
        cursor.execute('UPDATE guild_settings SET sugestao_channel_id = NULL WHERE guild_id = ?', (guild_id,))
        conn.commit()
        conn.close()
        await ctx.send('Retirei o canal de sugestões com sucesso!')

async def setup(bot):
    await bot.add_cog(DelSugestao(bot))