from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from requests_oauthlib import OAuth2Session
import os
import requests

# IMPORTANT: Only set this to '1' for local development with HTTP. NEVER in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# Flask Session Secret Key (IMPORTANT: Change this to a strong, random value in production)
app.config['SECRET_KEY'] = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking modifications for performance
db = SQLAlchemy(app)

# Discord OAuth2 Configuration
# IMPORTANT: Replace with your actual Client ID and Client Secret
app.config['DISCORD_CLIENT_ID'] = '1370143300228747284'
app.config['DISCORD_CLIENT_SECRET'] = '8NRUYTkZlpKUlW1C8qZyPEPdoZ2yRtj3'
app.config['DISCORD_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'

# Discord OAuth2 scopes (what information you want to access)
# 'identify' for basic user information, 'guilds' to get list of guilds the user is in
DISCORD_API_BASE_URL = 'https://discord.com/api'
DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + '/oauth2/authorize'
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + '/oauth2/token'

# Define a simple model for Guild settings
class Guild(db.Model):
    id = db.Column(db.BigInteger, primary_key=True) # Discord Guild IDs are large integers
    custom_prefix = db.Column(db.String(10), default='!') # Default prefix

    def __repr__(self):
        return f"Guild('{self.id}', '{self.custom_prefix}')"

# Define a User model to store logged-in Discord users
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True) # Discord User ID
    username = db.Column(db.String(80), nullable=False)
    discriminator = db.Column(db.String(4), nullable=False) # e.g., '0001'

    def __repr__(self):
        return f"User('{self.username}#{self.discriminator}', '{self.id}')"

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def home():
    user = session.get('discord_user')
    return render_template('index.html', user=user)

# Discord OAuth2 login route
@app.route('/login')
def login():
    discord = OAuth2Session(app.config['DISCORD_CLIENT_ID'], redirect_uri=app.config['DISCORD_REDIRECT_URI'],
                            scope=['identify', 'guilds'])
    authorization_url, state = discord.authorization_url(DISCORD_AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

# Discord OAuth2 callback route
@app.route('/callback')
def callback():
    if request.url_rule.endpoint != 'callback': # Ensure this route is handled by the callback function
        return "Invalid callback URL.", 400

    discord = OAuth2Session(app.config['DISCORD_CLIENT_ID'], redirect_uri=app.config['DISCORD_REDIRECT_URI'],
                            state=session['oauth2_state'])
    token = discord.fetch_token(DISCORD_TOKEN_URL,
                                client_secret=app.config['DISCORD_CLIENT_SECRET'],
                                authorization_response=request.url)

    session['discord_token'] = token

    # Fetch user details
    user_info = discord.get(DISCORD_API_BASE_URL + '/users/@me').json()
    session['discord_user'] = user_info

    # Check if user exists in database, if not, add them
    user_id = user_info['id']
    existing_user = User.query.get(user_id)

    if not existing_user:
        new_user = User(
            id=user_id,
            username=user_info['username'],
            discriminator=user_info['discriminator']
        )
        db.session.add(new_user)
        db.session.commit()
    # If the user exists, you could update their info here if needed
    # For now, we just ensure they are in the database on first login

    # Store avatar hash in session
    session['discord_user']['avatar_url'] = f"https://cdn.discordapp.com/avatars/{user_id}/{user_info['avatar']}.png" if user_info.get('avatar') else None

    # Fetch guilds (servers) the user is in
    guilds = discord.get(DISCORD_API_BASE_URL + '/users/@me/guilds').json()
    session['discord_guilds'] = guilds

    return redirect(url_for('dashboard')) # Redirect to a dashboard page

# Dummy dashboard route (we'll build this properly later)
@app.route('/dashboard')
def dashboard():
    if 'discord_user' not in session:
        return redirect(url_for('login'))

    user = session['discord_user']
    discord_guilds = session['discord_guilds']

    # List to store processed guilds with permissions and custom prefixes
    processed_guilds = []
    for guild_data in discord_guilds:
        guild_id = guild_data['id']
        permissions = int(guild_data['permissions']) # Permissions are usually strings, convert to int
        
        # Discord permission for MANAGE_GUILD is 0x20 (32 in decimal)
        can_manage = (permissions & 0x20) == 0x20 # Check if user has MANAGE_GUILD permission

        # Fetch custom prefix for the guild from the database
        guild_db_entry = Guild.query.filter_by(id=guild_id).first()
        custom_prefix = guild_db_entry.custom_prefix if guild_db_entry else '!' # Default to '!' if no entry

        processed_guilds.append({
            'id': guild_id,
            'name': guild_data['name'],
            'icon': guild_data['icon'],
            'owner': guild_data['owner'],
            'can_manage': can_manage,
            'custom_prefix': custom_prefix
        })
    
    # Sort guilds: manageable guilds first, then by name
    processed_guilds.sort(key=lambda g: (not g['can_manage'], g['name'].lower()))

    return render_template('dashboard.html', user=user, guilds=processed_guilds)

# Logout route
@app.route('/logout')
def logout():
    session.pop('discord_user', None)
    session.pop('discord_token', None)
    session.pop('discord_guilds', None)
    session.pop('oauth2_state', None)
    return redirect(url_for('home'))

# Example route to set and get a custom prefix for a guild
@app.route('/guild/<int:guild_id>', methods=['GET', 'POST'])
def guild_settings(guild_id):
    # Ensure user is logged in
    if 'discord_user' not in session:
        return jsonify({'success': False, 'message': 'Não autorizado.'}), 401

    # Check if the authenticated user has permissions to manage this guild
    user_guilds = session.get('discord_guilds', [])
    current_guild_data = next((g for g in user_guilds if g['id'] == str(guild_id)), None)

    if not current_guild_data:
        return jsonify({'success': False, 'message': 'Servidor não encontrado ou não gerenciável por você.'}), 403
    
    permissions = int(current_guild_data.get('permissions', 0))
    can_manage = (permissions & 0x20) == 0x20 # MANAGE_GUILD permission

    if not can_manage:
        return jsonify({'success': False, 'message': 'Você não tem permissão para gerenciar este servidor.'}), 403

    guild = Guild.query.get(guild_id)
    if not guild:
        # If guild not in DB, create it with default prefix
        guild = Guild(id=guild_id)
        db.session.add(guild)
        db.session.commit()

    if request.method == 'POST':
        data = request.get_json() # Get JSON data from AJAX request
        new_prefix = data.get('prefix')

        if new_prefix:
            guild.custom_prefix = new_prefix
            db.session.commit()
            return jsonify({'success': True, 'message': 'Prefixo atualizado com sucesso!', 'new_prefix': new_prefix})
        else:
            return jsonify({'success': False, 'message': 'Prefixo inválido.'}), 400
    
    # For GET requests (if someone tries to access /guild/ID directly)
    # You might want to remove this if you only want AJAX interaction
    return render_template('guild_settings.html', guild=guild)

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        to_email = request.form.get('to_email')

        # Prepare data to send to webhook.site
        payload = {
            'to_email': to_email,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

        # Send the POST request to webhook.site
        try:
            response = requests.post("https://api.webhook.site/send/email", data=payload)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return jsonify({'success': True, 'message': 'E-mail enviado com sucesso!'})
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar e-mail: {e}")
            return jsonify({'success': False, 'message': f'Erro ao enviar e-mail: {e}'}), 500
    return jsonify({'success': False, 'message': 'Método não permitido'}), 405

if __name__ == '__main__':
    # For development, you can create the database and tables here if not already done
    with app.app_context():
        db.create_all()
    app.run(debug=True) 