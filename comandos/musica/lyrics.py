import discord
from discord.ext import commands
import lyricsgenius
import os
from dotenv import load_dotenv
from comandos.musica.play import now_playing

load_dotenv()

GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')
if not GENIUS_TOKEN:
    print("Erro: O token do Genius não foi encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")
    genius = None
else:
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    genius.remove_section_headers = True
    genius.skip_artists = ['(Ft. ', 'Feat. ']


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lyrics', aliases=['letra'], help='Busca a letra de uma música.')
    @commands.bot_has_permissions(send_messages=True)
    async def lyrics_command(self, ctx, *, query=None):
        vc = ctx.voice_client
        musica_info = now_playing.get(ctx.guild.id)

        # Se nenhuma query for fornecida, usa a música atual
        if not query and musica_info:
            query = musica_info['title']
        elif not query:
            return await ctx.send("❌ Por favor, forneça o nome da música ou use o comando enquanto uma música está tocando.")

        # Busca a letra da música
        try:
            song = genius.search_song(query)
            if not song:
                return await ctx.send("❌ Não encontrei a letra para esta música.")

            lyrics_text = song.lyrics

            # Divide a letra em blocos menores para enviar
            chunks = [lyrics_text[i:i + 2000] for i in range(0, len(lyrics_text), 2000)]

            for chunk in chunks:
                embed = discord.Embed(
                    title=f"Letra: {song.title} por {song.artist}",
                    description=chunk,
                    color=0xE8E8E8
                )
                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao buscar a letra: {e}")


async def setup(bot):
    await bot.add_cog(Lyrics(bot))
