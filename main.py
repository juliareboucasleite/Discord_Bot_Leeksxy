import discord
from discord.ext import commands
import os
import logging
import asyncio
import sqlite3
import sys
from fuzzywuzzy import process
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("Erro: O token do Discord não foi encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

# Configurar FFmpeg
os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="'", intents=intents, help_command=None)

DATABASE = 'dados.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

# Função para inicializar o banco de dados
async def setup_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favoritas (
                user_id INTEGER,
                guild_id INTEGER,
                title TEXT,
                url TEXT,
                PRIMARY KEY (user_id, guild_id, url)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                guild_id INTEGER,
                user_id INTEGER,
                title TEXT,
                url TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_settings (
                guild_id INTEGER PRIMARY KEY,
                welcome_channel_id INTEGER,
                leave_channel_id INTEGER,
                autorole_id INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reaction_roles (
                guild_id INTEGER,
                message_id INTEGER,
                emoji TEXT,
                role_id INTEGER,
                PRIMARY KEY (guild_id, message_id, emoji)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                moderator_id INTEGER,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_economy (
                user_id INTEGER,
                guild_id INTEGER,
                balance INTEGER DEFAULT 0,
                last_daily TEXT,
                last_work TEXT,
                PRIMARY KEY (user_id, guild_id)
            )
        ''')
        conn.commit()
    print("【✔】Banco de dados inicializado e tabelas verificadas.")

@bot.event
async def on_ready():
    print(f"【✔】Bot {bot.user} está online e pronto!")
    if bot.user is not None:
        print(f"ID do Bot: {bot.user.id}")
    else:
        print("ID do Bot: desconhecido (bot.user é None)")
    print(f"Conectado em {len(bot.guilds)} servidores")
    await bot.change_presence(
        activity=discord.Streaming(
            name="Leeksxy",
            url="https://www.twitch.tv/leeksxy"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_name = ctx.message.content.split(' ')[0][len(ctx.prefix):]
        all_commands = [cmd.name for cmd in bot.commands]
        
        best_match = process.extractOne(command_name, all_commands)
        
        if best_match and best_match[1] >= 70:
            suggestion = best_match[0]
            embed = discord.Embed(
                title="❌ Comando Não Encontrado",
                description=f"O comando `'{command_name}` não existe. Você quis dizer `'{suggestion}`?",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Comando Não Encontrado",
                description=f"O comando `'{command_name}` não existe. Use `'ajuda` para ver a lista de comandos disponíveis.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permissões Insuficientes",
            description="Você não tem permissão para usar este comando.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Argumento Faltando",
            description=f"Faltou o argumento: {error.param.name}\nUse `'ajuda {ctx.command.name}` para ver como usar este comando.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    else:
        logger.error(f"Erro não tratado no comando '{ctx.command}': {error}")
        embed = discord.Embed(
            title="❌ Erro",
            description="Ocorreu um erro ao executar o comando. Por favor, tente novamente mais tarde.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT welcome_channel_id, autorole_id FROM guild_settings WHERE guild_id = ?", (member.guild.id,))
        settings = cursor.fetchone()

    if settings:
        welcome_channel_id, autorole_id = settings

        if welcome_channel_id:
            channel = bot.get_channel(welcome_channel_id)
            if isinstance(channel, (discord.TextChannel, discord.DMChannel)):
                embed = discord.Embed(
                    title="👋 Bem-Vindo(a)!",
                    description=f"Seja bem-vindo(a), {member.mention}, ao servidor **{member.guild.name}**!",
                    color=0x7289DA
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.set_footer(text=f"Membro #{len(member.guild.members)}")
                await channel.send(embed=embed)

        if autorole_id:
            role = member.guild.get_role(autorole_id)
            if role:
                try:
                    await member.add_roles(role)
                    logger.info(f"Cargo {role.name} atribuído a {member.name}")
                except discord.Forbidden:
                    logger.error(f"Permissões insuficientes para atribuir o cargo {role.name} para {member.name}")
                except Exception as e:
                    logger.error(f"Erro ao atribuir cargo a {member.name}: {e}")

@bot.event
async def on_member_remove(member):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT leave_channel_id FROM guild_settings WHERE guild_id = ?", (member.guild.id,))
        settings = cursor.fetchone()

    if settings and settings[0]:
        leave_channel_id = settings[0]
        channel = bot.get_channel(leave_channel_id)
        if isinstance(channel, (discord.TextChannel, discord.DMChannel)):
            embed = discord.Embed(
                title="👋 Adeus!",
                description=f"{member.display_name} deixou o servidor. Sentiremos sua falta!",
                color=0xFF0000
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        return

    guild_id = payload.guild_id
    message_id = payload.message_id

    if payload.emoji.id:
        normalized_emoji = f'a:{payload.emoji.name}:{payload.emoji.id}' if payload.emoji.animated else f'{payload.emoji.name}:{payload.emoji.id}'
    else:
        normalized_emoji = payload.emoji.name

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
                      (guild_id, message_id, normalized_emoji))
        result = cursor.fetchone()

    if result:
        role_id = result[0]
        guild = bot.get_guild(guild_id)
        if guild:
            role = guild.get_role(role_id)
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                logger.error(f"Membro com ID {payload.user_id} não encontrado na guild {guild_id}.")
                return

            if role and member:
                try:
                    await member.add_roles(role)
                    logger.info(f"Cargo {role.name} adicionado a {member.display_name} via reação.")
                except discord.Forbidden:
                    logger.error(f"Permissões insuficientes para adicionar o cargo {role.name} para {member.display_name}.")
                except Exception as e:
                    logger.error(f"Erro ao adicionar cargo via reação para {member.display_name}: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    guild_id = payload.guild_id
    message_id = payload.message_id

    if payload.emoji.id:
        normalized_emoji = f'a:{payload.emoji.name}:{payload.emoji.id}' if payload.emoji.animated else f'{payload.emoji.name}:{payload.emoji.id}'
    else:
        normalized_emoji = payload.emoji.name

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
                      (guild_id, message_id, normalized_emoji))
        result = cursor.fetchone()

    if result:
        role_id = result[0]
        guild = bot.get_guild(guild_id)
        if guild:
            role = guild.get_role(role_id)
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                logger.error(f"Membro com ID {payload.user_id} não encontrado na guild {guild_id}.")
                return

            if role and member:
                try:
                    await member.remove_roles(role)
                    logger.info(f"Cargo {role.name} removido de {member.display_name} via reação.")
                except discord.Forbidden:
                    logger.error(f"Permissões insuficientes para remover o cargo {role.name} de {member.display_name}.")
                except Exception as e:
                    logger.error(f"Erro ao remover cargo via reação de {member.display_name}: {e}")

async def setup_comandos():
    for folder in os.listdir("comandos"):
        if os.path.isdir(os.path.join("comandos", folder)):
            for file in os.listdir(os.path.join("comandos", folder)):
                if file.endswith(".py") and not file.startswith("__"):
                    try:
                        await bot.load_extension(f"comandos.{folder}.{file[:-3]}")
                        print(f"【✔】Comando {file[:-3]} carregado!")
                    except Exception as e:
                        print(f"【✘】Falha ao carregar o comando {file[:-3]}: {e}")

async def main():
    await setup_db()
    await setup_comandos()
    
    # Iniciar o bot
    if TOKEN is not None:
        await bot.start(TOKEN)
    else:
        print("Erro: Token do Discord não encontrado!")

# Configuração para o Gunicorn
from web_app import app as flask_app
from aiohttp import web

async def handle_health(request):
    return web.Response(text="OK")

async def init_app():
    app = web.Application()
    app.router.add_get('/healthz', handle_health)
    return app

app = init_app()

if __name__ == "__main__":
    asyncio.run(main())

# Note: Replace the token with your actual bot token.
# Ensure you keep your token secure and do not share it publicly.