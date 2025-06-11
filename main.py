import discord
from discord.ext import commands
import os
import logging
import asyncio
import sqlite3
from web_app import app # Importa a aplicação Flask
from waitress import serve # Importa o servidor WSGI
from fuzzywuzzy import process
import sys
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("Erro: O token do Discord não foi encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

# Configurar FFmpeg
os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="'", intents=intents, help_command=None)

DATABASE = 'dados.db'

# Função para inicializar o banco de dados
async def setup_db():
    conn = sqlite3.connect(DATABASE)
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
    conn.close()
    print("✅ Banco de dados inicializado e tabelas 'favoritas', 'history', 'guild_settings', 'reaction_roles', 'warnings' e 'user_economy' verificadas.")

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} está online e pronto!")
    print(f"ID do Bot: {bot.user.id}")
    print(f"Conectado em {len(bot.guilds)} servidores")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="comandos do bot | 'ajuda"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_name = ctx.message.content.split(' ')[0][len(bot.command_prefix):] # Remove o prefixo para pegar o nome do comando
        all_commands = [cmd.name for cmd in bot.commands] # Lista todos os comandos do bot
        
        # Tenta encontrar a melhor correspondência
        best_match = process.extractOne(command_name, all_commands)
        
        # fuzzywuzzy retorna (melhor_correspondencia, pontuação)
        # Definimos um limite de similaridade, por exemplo, 70
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
                description=f"O comando `'{command_name}` não existe.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
    else:
        # Outros erros de comando podem ser tratados aqui ou logados
        print(f"DEBUG: Ocorreu um erro no comando '{ctx.command}': {error}")
        # Para erros não tratados, você pode enviar uma mensagem genérica ou apenas logar.
        # await ctx.send(f"❌ Ocorreu um erro ao executar o comando: {error}")

@bot.event
async def on_member_join(member):
    # if member.bot: # Ignorar bots que entram no servidor
    #     return

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT welcome_channel_id, autorole_id FROM guild_settings WHERE guild_id = ?", (member.guild.id,))
    settings = cursor.fetchone()
    conn.close()

    if settings:
        welcome_channel_id, autorole_id = settings

        # Enviar mensagem de boas-vindas
        if welcome_channel_id:
            channel = bot.get_channel(welcome_channel_id)
            if channel:
                embed = discord.Embed(
                    title="👋 Bem-Vindo(a)!",
                    description=f"Seja bem-vindo(a), {member.mention}, ao servidor **{member.guild.name}**!",
                    color=0x7289DA # Cor azul Discord
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                embed.set_footer(text=f"Membro #{len(member.guild.members)}")
                await channel.send(embed=embed)

        # Atribuir autorole
        if autorole_id:
            role = member.guild.get_role(autorole_id)
            if role:
                try:
                    await member.add_roles(role)
                    print(f"✅ Cargo {role.name} atribuído a {member.name}")
                except discord.Forbidden:
                    print(f"❌ Permissões insuficientes para atribuir o cargo {role.name} para {member.name}")
                except Exception as e:
                    print(f"❌ Erro ao atribuir cargo a {member.name}: {e}")

@bot.event
async def on_member_remove(member):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT leave_channel_id FROM guild_settings WHERE guild_id = ?", (member.guild.id,))
    settings = cursor.fetchone()
    conn.close()

    if settings and settings[0]: # Se leave_channel_id estiver definido
        leave_channel_id = settings[0]
        channel = bot.get_channel(leave_channel_id)
        if channel:
            embed = discord.Embed(
                title="👋 Adeus!",
                description=f"{member.display_name} deixou o servidor. Sentiremos sua falta!",
                color=0xFF0000 # Cor vermelha
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    print(f"[DEBUG] on_raw_reaction_add acionado por: {payload.member.display_name} (ID: {payload.user_id})")
    if payload.member.bot: # Ignorar reações de bots
        print(f"[DEBUG] Reação de bot ({payload.member.display_name}) ignorada.")
        return

    guild_id = payload.guild_id
    message_id = payload.message_id
    print(f"[DEBUG] Guild ID: {guild_id}, Message ID: {message_id}, Emoji raw: {payload.emoji}")

    if payload.emoji.id: # É um emoji personalizado (tem um ID)
        if payload.emoji.animated:
            normalized_emoji = f'a:{payload.emoji.name}:{payload.emoji.id}'
        else:
            normalized_emoji = f'{payload.emoji.name}:{payload.emoji.id}'
    else: # É um emoji Unicode padrão (não tem ID)
        normalized_emoji = payload.emoji.name # Isso será '✅' para o emoji de checkmark
    print(f"[DEBUG] Emoji normalizado: {normalized_emoji}")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT role_id FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
                   (guild_id, message_id, normalized_emoji))
    result = cursor.fetchone()
    conn.close()

    if result:
        role_id = result[0]
        print(f"[DEBUG] Cargo ID encontrado no DB: {role_id}")
        guild = bot.get_guild(guild_id)
        if guild:
            role = guild.get_role(role_id)
            try:
                member = await guild.fetch_member(payload.user_id)
                print(f"[DEBUG] Membro fetch: {member.display_name} (ID: {member.id})")
            except discord.NotFound:
                print(f"[DEBUG] Membro com ID {payload.user_id} não encontrado na guild {guild_id}.")
                member = None # Define como None se não encontrar

            if role and member:
                print(f"[DEBUG] Tentando adicionar cargo {role.name} a {member.display_name}.")
                try:
                    await member.add_roles(role)
                    print(f"✅ Cargo {role.name} adicionado a {member.display_name} via reação.")
                except discord.Forbidden:
                    print(f"❌ Permissões insuficientes para adicionar o cargo {role.name} para {member.display_name}.")
                except Exception as e:
                    print(f"❌ Erro ao adicionar cargo via reação para {member.display_name}: {e}")
            else:
                print(f"[DEBUG] Role ou Member é None. Role: {bool(role)}, Member: {bool(member)}")
        else:
            print(f"[DEBUG] Guild com ID {guild_id} não encontrada.")
    else:
        print(f"[DEBUG] Nenhuma configuração de cargo por reação encontrada para Message ID: {message_id}, Emoji: {normalized_emoji}")

@bot.event
async def on_raw_reaction_remove(payload):
    print(f"[DEBUG] on_raw_reaction_remove acionado por: {payload.user_id}")
    guild_id = payload.guild_id
    message_id = payload.message_id

    # Quando a reação é removida por um bot, o user_id é o ID do bot.
    # Se o usuário é o próprio bot, não faça nada.
    if payload.user_id == bot.user.id:
        print(f"[DEBUG] Reação removida pelo próprio bot ({payload.user_id}) ignorada.")
        return

    if payload.emoji.id: # É um emoji personalizado (tem um ID)
        if payload.emoji.animated:
            normalized_emoji = f'a:{payload.emoji.name}:{payload.emoji.id}'
        else:
            normalized_emoji = f'{payload.emoji.name}:{payload.emoji.id}'
    else: # É um emoji Unicode padrão (não tem ID)
        normalized_emoji = payload.emoji.name
    print(f"[DEBUG] Guild ID: {guild_id}, Message ID: {message_id}, Emoji normalizado: {normalized_emoji}")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT role_id FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
                   (guild_id, message_id, normalized_emoji))
    result = cursor.fetchone()
    conn.close()

    if result:
        role_id = result[0]
        print(f"[DEBUG] Cargo ID encontrado no DB para remoção: {role_id}")
        guild = bot.get_guild(guild_id)
        if guild:
            role = guild.get_role(role_id)
            try:
                member = await guild.fetch_member(payload.user_id)
                print(f"[DEBUG] Membro fetch para remoção: {member.display_name} (ID: {member.id})")
            except discord.NotFound:
                print(f"[DEBUG] Membro com ID {payload.user_id} não encontrado na guild {guild_id} para remoção.")
                member = None

            if role and member:
                print(f"[DEBUG] Tentando remover cargo {role.name} de {member.display_name}.")
                try:
                    await member.remove_roles(role)
                    print(f"✅ Cargo {role.name} removido de {member.display_name} via remoção de reação.")
                except discord.Forbidden:
                    print(f"❌ Permissões insuficientes para remover o cargo {role.name} de {member.display_name}.")
                except Exception as e:
                    print(f"❌ Erro ao remover cargo via reação para {member.display_name}: {e}")
            else:
                print(f"[DEBUG] Role ou Member é None para remoção. Role: {bool(role)}, Member: {bool(member)}")
        else:
            print(f"[DEBUG] Guild com ID {guild_id} não encontrada para remoção.")
    else:
        print(f"[DEBUG] Nenhuma configuração de cargo por reação encontrada para remoção para Message ID: {message_id}, Emoji: {normalized_emoji}")

async def setup_comandos():
    print("🔄 Iniciando carregamento dos comandos...")
    for root, _, files in os.walk("./comandos"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.splitext(os.path.relpath(os.path.join(root, file), "./"))[0].replace(os.sep, ".")
                if file == "utils.py":  # Ignorar o arquivo utils.py
                    print(f"Skipping util file: {path}")
                    continue
                print(f"🔌 Carregando: {path}")
                try:
                    await bot.load_extension(path)
                    print(f"✅ Comando {path} carregado com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao carregar {path}: {e}")

async def start_web_server():
    print("🌐 Iniciando servidor web (Flask) em http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)

async def main():
    await setup_db()
    await setup_comandos()
    
    # Inicia o servidor web em uma tarefa separada, sem bloquear o bot
    asyncio.create_task(start_web_server())
    
    print("✅ Comandos carregados e servidor web iniciado, iniciando o bot...")
    await bot.start(TOKEN)

if __name__ == "__main__":
    bot.run_webserver.start()
    bot.run()

# Note: Replace the token with your actual bot token.
# Ensure you keep your token secure and do not share it publicly.