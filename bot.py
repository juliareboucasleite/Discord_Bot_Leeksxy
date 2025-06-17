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
    print("✅ Banco de dados inicializado e tabelas verificadas.")

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} está online e pronto!")
    print(f"ID do Bot: {bot.user.id}")
    print(f"Conectado em {len(bot.guilds)} servidores")
    await bot.change_presence(
        activity=discord.Streaming(
            name="Leeksxy",
            url="https://www.twitch.tv/leeksxy"
        )
    )

async def setup_comandos():
    for filename in os.listdir('./comandos'):
        if filename.endswith('.py'):
            await bot.load_extension(f'comandos.{filename[:-3]}')
    print("✅ Comandos carregados com sucesso!")

async def main():
    await setup_db()
    await setup_comandos()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main()) 