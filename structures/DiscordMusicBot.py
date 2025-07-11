import discord
from discord.ext import commands
from structures.Logger import Logger
import os

class DiscordMusicBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = Logger("Logs.log")
        self.commands_ran = 0
        self.songs_played = 0

    async def on_ready(self):
        self.logger.log(f"Bot conectado como {self.user}")

    async def setup_hook(self):
        # Carrega todos os cogs da pasta comandos/musica
        musica_path = os.path.join(os.path.dirname(__file__), '..', 'comandos', 'musica')
        musica_path = os.path.abspath(musica_path)
        for filename in os.listdir(musica_path):
            if filename.endswith(".py") and filename != "__init__.py":
                cog_name = f"comandos.musica.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    self.logger.log(f"Cog carregado: {cog_name}")
                except Exception as e:
                    self.logger.log(f"Erro ao carregar {cog_name}: {e}")
        # Carrega o EpicPlayer
        try:
            await self.load_extension("structures.EpicPlayer")
            self.logger.log("Cog carregado: structures.EpicPlayer")
        except Exception as e:
            self.logger.log(f"Erro ao carregar EpicPlayer: {e}")

# Exemplo de uso:
# bot = DiscordMusicBot(command_prefix="!", intents=discord.Intents.all())
# bot.run("SEU_TOKEN")
