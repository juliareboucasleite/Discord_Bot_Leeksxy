from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import os
import re # Import the regular expression module
import requests # Import the requests library
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder='web_panel/templates',
            static_folder='web_panel/static')

# --- Discord OAuth2 Configuration ---
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a_very_long_and_random_string_for_security')

DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')

if not all([DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI]):
    raise ValueError("Variáveis de ambiente DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET ou DISCORD_REDIRECT_URI não configuradas.")

# Discord API Endpoints
DISCORD_AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify%20guilds"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_BASE_URL = "https://discord.com/api/users/@me"
DISCORD_GUILDS_URL = "https://discord.com/api/users/@me/guilds"

# Exemplo de dados de usuário (para simular o login)
# Em uma aplicação real, isso viria de uma sessão de login
# This will now be superseded by actual Discord user data from session
USER_DATA = {
    "username": "Teste",
    "discriminator": "1234",
    "avatar_url": "https://cdn.discordapp.com/embed/avatars/0.png" # Exemplo de avatar
}

# Function to dynamically load commands from the 'comandos' directory
def load_commands():
    commands_list = []
    commands_base_dir = 'comandos' # Caminho base para o diretório de comandos

    # Percorrer recursivamente os subdiretórios
    for root, dirs, files in os.walk(commands_base_dir):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    command_name = None
                    command_description = "Nenhuma descrição disponível."

                    # Etapa 1: Extrair o conteúdo dos argumentos do decorador
                    # Este padrão visa obter tudo dentro do primeiro @commands.command(...)
                    decorator_match = re.search(r"@commands\.command\s*\((.*?)\)", content, re.DOTALL)
                    
                    if decorator_match:
                        args_string = decorator_match.group(1) # Esta é a string dentro dos parênteses

                        # Etapa 2: Extrair 'name' da string de argumentos
                        name_match = re.search(r"name=['\"](.+?)['\"]", args_string)
                        if name_match:
                            command_name = name_match.group(1)

                        # Etapa 3: Extrair 'description' da string de argumentos
                        description_match = re.search(r"description=['\"](.+?)['\"]", args_string)
                        if description_match:
                            command_description = description_match.group(1)
                    
                    # Fallback para o nome do arquivo se o nome do comando não for encontrado no decorador
                    if not command_name:
                        command_name = os.path.splitext(filename)[0]
                   
                    commands_list.append({"name": command_name, "description": command_description})

    return commands_list

# Global variable to store commands (cached)
ALL_COMMANDS = load_commands()

@app.route('/')
def index():
    # Fetch user from session if logged in
    user_info = session.get('discord_user')
    return render_template('index.html', user=user_info)

@app.route('/comandos')
def comandos():
    # Fetch user from session if logged in
    user_info = session.get('discord_user')
    return render_template('comandos.html', user=user_info, commands=ALL_COMMANDS)

@app.route('/send_email', methods=['POST'])
def send_email():
    # Em uma aplicação real, você integraria com um serviço de envio de e-mail aqui
    # Por exemplo, usando a biblioteca SMTPLIB ou um serviço como SendGrid/Mailgun
    data = request.get_json()
    print(f"Recebido e-mail de: {data.get('name')} ({data.get('email')})")
    print(f"Assunto: {data.get('subject')}")
    print(f"Mensagem: {data.get('message')}")
    
    # Aqui você adicionaria a lógica para enviar o e-mail real
    # Por enquanto, apenas retornamos uma resposta de sucesso
    return jsonify({"success": True, "message": "E-mail enviado com sucesso!"})

@app.route('/invite')
def invite():
    # Redireciona para o URL de autorização do bot no Discord
    return redirect(DISCORD_AUTH_URL)

@app.route('/dashboard')
def dashboard():
    user_info = session.get('discord_user')
    guilds_data = []

    if user_info and 'access_token' in session:
        headers = {'Authorization': f'Bearer {session["access_token"]}'}
        try:
            guilds_response = requests.get(DISCORD_GUILDS_URL, headers=headers)
            guilds_response.raise_for_status() # Raise an exception for HTTP errors
            guilds_data = []
            for guild in guilds_response.json():
                # Filter for guilds where the bot is in
                # For a real bot, you'd check if the bot is in the guild
                # and if the user has permissions to manage the bot
                guilds_data.append({
                    "id": guild['id'],
                    "name": guild['name'],
                    "icon": guild['icon'],
                    "can_manage": True if guild['owner'] else False, # Simplified: assume owner can manage
                    "custom_prefix": "'" # Placeholder, ideally fetched from bot's actual data
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching guilds: {e}")
            # Handle error, maybe redirect to login or show a message
            pass # Continue with empty guilds_data

    return render_template('dashboard.html', user=user_info, guilds=guilds_data)

@app.route('/login')
def login():
    return redirect(DISCORD_AUTH_URL)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No authorization code provided", 400

    # Exchange authorization code for access token
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': 'identify guilds'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        token_response = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
        token_response.raise_for_status()
        token_json = token_response.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return "Error: Could not retrieve access token.", 500

        # Fetch user info
        user_headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(DISCORD_API_BASE_URL, headers=user_headers)
        user_response.raise_for_status()
        user_json = user_response.json()

        # Store user info and access token in session
        session['discord_user'] = {
            'id': user_json.get('id'),
            'username': user_json.get('username'),
            'discriminator': user_json.get('discriminator'),
            'avatar_url': f"https://cdn.discordapp.com/avatars/{user_json.get('id')}/{user_json.get('avatar')}.png" if user_json.get('avatar') else f"https://cdn.discordapp.com/embed/avatars/{int(user_json.get('discriminator', 0)) % 5}.png"
        }
        session['access_token'] = access_token # Store access token to fetch guilds later

        return redirect(url_for('index'))

    except requests.exceptions.RequestException as e:
        return f"Error during OAuth2 process: {e}", 500

@app.route('/logout')
def logout():
    session.pop('discord_user', None)
    session.pop('access_token', None)
    return redirect(url_for('index'))

@app.route('/healthz', methods=['GET'])
def health_check():
    return "OK", 200

# Removendo o bloco if __name__ == '__main__', pois o Flask será iniciado pelo main.py
# if __name__ == '__main__':
#     app.run(debug=False) 