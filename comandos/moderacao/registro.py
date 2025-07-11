import discord
from discord.ext import commands
import sqlite3
from typing import Optional

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'dados.db'

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)

    @commands.group(name='registro', invoke_without_command=True, help='Configurações do sistema de registro.')
    @commands.has_permissions(administrator=True)
    async def registro(self, ctx):
        embed = discord.Embed(
            title='Ajuda | Registro',
            description='Comandos disponíveis para configuração do sistema de registro:',
            color=0xE74C3C
        )
        embed.add_field(name='registro registrador <@cargo>', value='Define ou remove cargos de registrador.', inline=False)
        embed.add_field(name='registro novato <@cargo>', value='Define o cargo de novato (dado a novos membros).', inline=False)
        embed.add_field(name='registro registrados <@cargo>', value='Define ou remove cargos de registrado.', inline=False)
        embed.add_field(name='registro resetar', value='Reseta todas as configurações de registro.', inline=False)
        await ctx.send(embed=embed)

    @registro.command(name='registrador')
    @commands.has_permissions(administrator=True)
    async def registrador(self, ctx, role: Optional[discord.Role] = None):
        if not role:
            return await ctx.send('Mencione o cargo de registrador.')
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registro_config (
            guild_id INTEGER PRIMARY KEY, registrador_roles TEXT, novato_role INTEGER, registrados_roles TEXT
        )''')
        cursor.execute('SELECT registrador_roles FROM registro_config WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        roles = set(map(int, result[0].split(','))) if result and result[0] else set()
        if role.id in roles:
            roles.remove(role.id)
            action = 'removido'
        else:
            if len(roles) >= 10:
                conn.close()
                return await ctx.send('Você já definiu 10 ou mais cargos de registrador.')
            roles.add(role.id)
            action = 'adicionado'
        roles_str = ','.join(map(str, roles))
        cursor.execute('INSERT OR REPLACE INTO registro_config (guild_id, registrador_roles) VALUES (?, ?)', (guild_id, roles_str))
        conn.commit()
        conn.close()
        await ctx.send(f'Cargo {role.mention} {action} como registrador.')

    @registro.command(name='novato')
    @commands.has_permissions(administrator=True)
    async def novato(self, ctx, role: Optional[discord.Role] = None):
        if not role:
            return await ctx.send('Mencione o cargo de novato.')
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registro_config (
            guild_id INTEGER PRIMARY KEY, registrador_roles TEXT, novato_role INTEGER, registrados_roles TEXT
        )''')
        cursor.execute('INSERT OR REPLACE INTO registro_config (guild_id, novato_role) VALUES (?, ?)', (guild_id, role.id))
        conn.commit()
        conn.close()
        await ctx.send(f'Cargo {role.mention} definido como cargo de novato.')

    @registro.command(name='registrados')
    @commands.has_permissions(administrator=True)
    async def registrados(self, ctx, role: Optional[discord.Role] = None):
        if not role:
            return await ctx.send('Mencione o cargo de registrado.')
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registro_config (
            guild_id INTEGER PRIMARY KEY, registrador_roles TEXT, novato_role INTEGER, registrados_roles TEXT
        )''')
        cursor.execute('SELECT registrados_roles FROM registro_config WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()
        roles = set(map(int, result[0].split(','))) if result and result[0] else set()
        if role.id in roles:
            roles.remove(role.id)
            action = 'removido'
        else:
            if len(roles) >= 10:
                conn.close()
                return await ctx.send('Você já definiu 10 ou mais cargos de registrado.')
            roles.add(role.id)
            action = 'adicionado'
        roles_str = ','.join(map(str, roles))
        cursor.execute('INSERT OR REPLACE INTO registro_config (guild_id, registrados_roles) VALUES (?, ?)', (guild_id, roles_str))
        conn.commit()
        conn.close()
        await ctx.send(f'Cargo {role.mention} {action} como registrado.')

    @registro.command(name='resetar')
    @commands.has_permissions(administrator=True)
    async def resetar(self, ctx):
        guild_id = ctx.guild.id
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registro_config WHERE guild_id = ?', (guild_id,))
        conn.commit()
        conn.close()
        await ctx.send('Configurações de registro resetadas com sucesso!')

async def setup(bot):
    await bot.add_cog(Registro(bot))
