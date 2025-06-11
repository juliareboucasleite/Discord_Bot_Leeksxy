import discord
from discord.ext import commands
import sqlite3
from .utils import now_playing

# A variável global 'favoritos' não será mais usada para persistência.
# Continuaremos usando-a como um cache se necessário, mas o foco será no DB.

class Favoritar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favoritas (
                user_id INTEGER,
                title TEXT,
                url TEXT,
                PRIMARY KEY (user_id, guild_id, url)
            )
        ''')
        conn.commit()
        conn.close()

    @commands.command(name="favoritar", aliases=["fav", "adicionar_fav"])
    async def favoritar_command(self, ctx):
        if not ctx.guild.voice_client or not ctx.guild.voice_client.is_playing():
            return await ctx.send("❌ Nenhuma música está tocando no momento para ser favoritada.")

        # Acessa as informações da música tocando para este servidor
        current_song_info = now_playing.get(ctx.guild.id, {})

        title = current_song_info.get('title')
        url = current_song_info.get('url')

        if not title or not url:
            return await ctx.send("❌ Não consegui obter as informações da música atual.")

        user_id = ctx.author.id
        guild_id = ctx.guild.id

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO favoritas (user_id, guild_id, title, url) VALUES (?, ?, ?, ?)", (user_id, guild_id, title, url))
            conn.commit()
            embed = discord.Embed(
                title="❤️ Música Favoritada!",
                description=f"A música [{title}]({url}) foi adicionada aos seus favoritos.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed)
        except sqlite3.IntegrityError:
            embed = discord.Embed(
                title="⚠️ Já Favoritada",
                description=f"A música [{title}]({url}) já está nos seus favoritos.",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
        finally:
            conn.close()

    @commands.command(name="desfavoritar", aliases=["desfav", "remover_fav"])
    async def desfavoritar_command(self, ctx, *, music_title_or_url: str):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM favoritas WHERE user_id = ? AND guild_id = ? AND (title LIKE ? OR url LIKE ?)", (user_id, guild_id, f'%{music_title_or_url}%', f'%{music_title_or_url}%'))
        conn.commit()
        if cursor.rowcount > 0:
            embed = discord.Embed(
                title="💔 Música Desfavoritada",
                description=f"A música contendo `{music_title_or_url}` foi removida dos seus favoritos.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❓ Música Não Encontrada",
                description=f"Não encontrei nenhuma música `{music_title_or_url}` em seus favoritos para desfavoritar.",
                color=0xFFD700
            )
            await ctx.send(embed=embed)
        conn.close()

    @commands.command(name="favoritas", aliases=["favs", "minhas_favoritas"])
    async def listar_favoritas_command(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT title, url FROM favoritas WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
        favoritas = cursor.fetchall()
        conn.close()

        if not favoritas:
            embed = discord.Embed(
                title="⭐ Suas Músicas Favoritas",
                description="Você ainda não adicionou nenhuma música aos seus favoritos.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed)

        description = "\n".join([f"• [{title}]({url})" for title, url in favoritas])
        embed = discord.Embed(
            title="⭐ Suas Músicas Favoritas",
            description=description,
            color=0xE8E8E8
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Favoritar(bot))
