import os
import requests
from flask import Flask, redirect, url_for, session, request, render_template, flash
from flask_session import Session
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecret')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:5000/callback')
API_BASE_URL = 'https://discord.com/api'
OAUTH_SCOPE = 'identify guilds'

# Utilitário para checar login
def is_logged_in():
    return 'discord_user' in session

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html', logged_in=is_logged_in(), user=session.get('discord_user'))

# Login via Discord
@app.route('/login')
def login():
    params = {
        'client_id': DISCORD_CLIENT_ID,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'response_type': 'code',
        'scope': OAUTH_SCOPE
    }
    return redirect(f"{API_BASE_URL}/oauth2/authorize?{urlencode(params)}")

# Callback do Discord
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        flash('Erro ao autenticar com o Discord.', 'danger')
        return redirect(url_for('index'))
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': OAUTH_SCOPE
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(f'{API_BASE_URL}/oauth2/token', data=data, headers=headers)
    if r.status_code != 200:
        flash('Erro ao obter token do Discord.', 'danger')
        return redirect(url_for('index'))
    tokens = r.json()
    session['discord_token'] = tokens['access_token']
    # Buscar dados do usuário
    user = requests.get(f'{API_BASE_URL}/users/@me', headers={'Authorization': f"Bearer {tokens['access_token']}"}).json()
    session['discord_user'] = user
    # Buscar guilds do usuário
    guilds = requests.get(f'{API_BASE_URL}/users/@me/guilds', headers={'Authorization': f"Bearer {tokens['access_token']}"}).json()
    session['discord_guilds'] = guilds
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    user = session['discord_user']
    guilds = session.get('discord_guilds', [])
    return render_template('dashboard.html', user=user, guilds=guilds)

@app.route('/comandos')
def comandos():
    return render_template('comandos.html', logged_in=is_logged_in(), user=session.get('discord_user'))

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', logged_in=is_logged_in(), user=session.get('discord_user'))

if __name__ == '__main__':
    app.run(debug=True) 