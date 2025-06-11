import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

# A variável global 'history' não será mais usada, pois os dados serão lidos do DB.

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    # on_command_completion para o comando play não é mais necessário aqui,
    # pois o registro no histórico é feito diretamente no play.py.
    # @commands.Cog.listener()
    # async def on_command_completion(self, ctx):
    #     if ctx.command.name == "play":
    #         song = now_playing.get(ctx.guild.id)
    #         if song:
    #             history.setdefault(ctx.guild.id, []).append(song)

    @commands.command(name="history", aliases=["historico"])
    async def history_command(self, ctx, limit: int = 10):
        if limit < 1 or limit > 20:
            embed = discord.Embed(
                title="⚠️ Limite Inválido",
                description="O limite de músicas no histórico deve ser entre 1 e 20.",
                color=0xFFD700
            )
            return await ctx.send(embed=embed)

        user_id = ctx.author.id
        guild_id = ctx.guild.id

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, url, timestamp 
            FROM history 
            WHERE user_id = ? AND guild_id = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, guild_id, limit))
        history_records = cursor.fetchall()
        conn.close()

        if not history_records:
            embed = discord.Embed(
                title="📜 Histórico Vazio",
                description="Você ainda não tem histórico de músicas neste servidor.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed)

        description = ""
        for i, (title, url, timestamp) in enumerate(history_records, 1):
            date_obj = datetime.fromisoformat(timestamp) # Assumindo que timestamp é uma string ISO formatada
            description += f"**{i}.** [{title}]({url}) - <t:{int(date_obj.timestamp())}:R>\n"

        embed = discord.Embed(
            title="📜 Seu Histórico de Músicas",
            description=description,
            color=0xE8E8E8
        )
        embed.set_footer(text=f"Total de músicas no histórico: {len(history_records)}")
        await ctx.send(embed=embed)

    @commands.command(name="clearhistory", aliases=["limparhistorico"])
    async def clear_history_command(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM history WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        total_records = cursor.fetchone()[0]

        if total_records == 0:
            embed = discord.Embed(
                title="❌ Histórico Vazio",
                description="Você não tem histórico de músicas para limpar neste servidor.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        cursor.execute('DELETE FROM history WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
        conn.commit()
        conn.close()

        embed = discord.Embed(
            title="🗑️ Histórico Limpo",
            description=f"Seu histórico de **{total_records}** músicas foi limpo com sucesso neste servidor.",
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(History(bot))
