import discord
from discord.ext import commands
import sqlite3
from typing import Optional

class Sugestao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='sugestao', help='Envia uma sugestão para o canal de sugestões configurado.')
    async def sugestao(self, ctx, *, sugestao: Optional[str] = None):
        if not sugestao:
            return await ctx.send('Diga depois da sintaxe a sua sugestão.')
        if len(sugestao) > 500:
            return await ctx.send('Faça uma sugestão menor!')
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT sugestao_channel_id FROM guild_settings WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        conn.close()
        if not result or not result[0]:
            return await ctx.send('O canal de sugestões ainda não foi setado! Use o comando de configuração para definir.')
        canal = ctx.guild.get_channel(result[0])
        if not canal:
            return await ctx.send('O canal de sugestões configurado não foi encontrado.')
        embed = discord.Embed(
            title=f'Sugestão - {ctx.author.display_name}',
            description=f'Sugestão: {sugestao}',
            color=0x7289DA
        )
        embed.set_footer(text=f'id do autor: {ctx.author.id}')
        embed.timestamp = discord.utils.utcnow()
        msg = await canal.send(embed=embed)
        await msg.add_reaction('❌')
        await msg.add_reaction('✅')
        await ctx.send('Enviei a sugestão com sucesso!')

async def setup(bot):
    await bot.add_cog(Sugestao(bot))