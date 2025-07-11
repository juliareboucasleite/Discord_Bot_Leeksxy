import discord
from discord.ext import commands
import sqlite3
from typing import Optional
from datetime import datetime

class Registrar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.command(name='registrar', help='Registra um usuário como membro do servidor.')
    @commands.has_permissions(administrator=True)
    async def registrar(self, ctx, member: Optional[discord.Member] = None):
        try:
            await ctx.message.delete()
        except Exception:
            pass
        if not member:
            return await ctx.send('Mencione o usuário a ser registrado.')
        if member.bot:
            return await ctx.send('Não é possível registrar bots.')
        if member.id == ctx.author.id:
            return await ctx.send('Não é possível registrar a si mesmo.')
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        # Buscar cargos de novato e registrado
        cursor.execute('SELECT autorole_id FROM guild_settings WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            await ctx.send('O cargo de novato não foi definido neste servidor.')
            conn.close()
            return
        novato_role = ctx.guild.get_role(result[0])
        if not novato_role or novato_role not in member.roles:
            await ctx.send('O usuário mencionado não possui o cargo de novato.')
            conn.close()
            return
        # Cargo de registrado (pode ser uma lista, aqui exemplo: "Registrado")
        registrado_role = discord.utils.get(ctx.guild.roles, name="Registrado")
        if not registrado_role:
            registrado_role = await ctx.guild.create_role(name="Registrado", reason="Cargo de registrado criado automaticamente.")
        await member.remove_roles(novato_role, reason="Registro efetuado")
        await member.add_roles(registrado_role, reason="Registro efetuado")
        # Contagem de registros por registrador (simples, pode ser expandido)
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
            guild_id INTEGER, registrador_id INTEGER, registrado_id INTEGER, data TEXT
        )''')
        cursor.execute('INSERT INTO registros (guild_id, registrador_id, registrado_id, data) VALUES (?, ?, ?, ?)',
                       (guild_id, ctx.author.id, member.id, datetime.utcnow().isoformat()))
        conn.commit()
        # Mensagem de sucesso
        embed = discord.Embed(
            title='Registro Efetuado',
            description=f'{member.mention} foi registrado com sucesso por {ctx.author.mention}! Bem-vindo(a)!',
            color=0xE74C3C
        )
        await ctx.send(embed=embed)
        # Mensagem privada
        try:
            await member.send(f'Você foi registrado no servidor **{ctx.guild.name}**!')
        except Exception:
            pass
        conn.close()

async def setup(bot):
    await bot.add_cog(Registrar(bot))
