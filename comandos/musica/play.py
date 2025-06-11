import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os
import json
import sqlite3
from .utils import now_playing, looping

queue = {}

def get_queue(guild_id):
    return queue.setdefault(guild_id, [])

def is_url(text):
    return text.startswith("http://") or text.startswith("https://")

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Você precisa estar em um canal de voz.")

        channel = ctx.author.voice.channel
        
        if not channel.permissions_for(ctx.guild.me).connect:
            return await ctx.send("❌ Não tenho permissão para entrar no canal de voz.")
        if not channel.permissions_for(ctx.guild.me).speak:
            return await ctx.send("❌ Não tenho permissão para falar no canal de voz.")

        try:
            if not ctx.voice_client:
                await channel.connect()
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
        except Exception as e:
            return await ctx.send(f"❌ Erro ao conectar ao canal de voz: {e}")

        ytdl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'no_warnings': False,
            'default_search': 'auto',
            'extract_flat': False,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        FFMPEG_EXECUTABLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ffmpeg.exe'))
        print(f"DEBUG: FFmpeg Executable Path: {FFMPEG_EXECUTABLE}")

        async with ctx.typing():
            try:
                with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                    info = ydl.extract_info(search, download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    
                    url = info.get('url')
                    if not url:
                        ytdl_opts_stream = {
                            'format': 'bestaudio/best',
                            'quiet': True,
                            'no_warnings': True,
                            'extract_flat': False,
                            'noplaylist': True,
                        }
                        with yt_dlp.YoutubeDL(ytdl_opts_stream) as ydl_stream:
                            stream_info = ydl_stream.extract_info(search, download=False)
                            if 'entries' in stream_info:
                                stream_info = stream_info['entries'][0]
                            url = stream_info.get('url')

                    if not url:
                        return await ctx.send("❌ Não encontrei nenhuma URL de áudio válida para sua busca.")

                    title = info.get('title', 'Título desconhecido')
                    duration = info.get('duration', 0)
                    
                    print(f"DEBUG: yt-dlp Info: {json.dumps(info, indent=2)}")
                    print(f"DEBUG: Final URL to play: {url}")

                    q = get_queue(ctx.guild.id)
                    q.append({'url': url, 'title': title, 'author': ctx.author, 'duration': duration})

                    if not ctx.voice_client.is_playing():
                        await self.play_next(ctx)
                    else:
                        embed = discord.Embed(
                            title="📥 Adicionado à Fila",
                            description=f"**[{title}]({url})**",
                            color=0xE8E8E8
                        )
                        if duration:
                            embed.add_field(name="⏱️ Duração", value=f"{duration//60}:{duration%60:02d}", inline=True)
                            embed.add_field(name="👤 Pedido por", value=f"{ctx.author.name}", inline=True)
                        embed.set_footer(text=f"👤 Pedido por: {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                        await ctx.send(embed=embed)

            except Exception as e:
                print(f"ERROR: Ocorreu um erro no yt-dlp ou na busca: {e}")
                await ctx.send(f"❌ Ocorreu um erro ao processar sua solicitação: {e}")

    async def play_next(self, ctx):
        q = get_queue(ctx.guild.id)
        if not q:
            await ctx.send("✅ Fila finalizada. O bot permanecerá no canal.")
            # Reset now_playing for this guild when queue is empty
            now_playing[ctx.guild.id] = {'title': 'Nenhuma música tocando', 'url': None, 'requester': None}
            looping[ctx.guild.id] = False
            return

        song_info = q.pop(0)
        url = song_info['url']
        title = song_info['title']
        author = song_info['author']
        duration = song_info['duration']

        now_playing[ctx.guild.id] = {'title': title, 'url': url, 'requester': author.display_name}

        conn = sqlite3.connect('dados.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO history (guild_id, user_id, title, url)
                VALUES (?, ?, ?, ?)
            ''',
            (ctx.guild.id, author.id, title, url))
            conn.commit()
        except Exception as e:
            print(f"ERROR: Erro ao salvar no histórico: {e}")
        finally:
            conn.close()

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -b:a 192k'
        }

        FFMPEG_EXECUTABLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ffmpeg.exe'))

        try:
            print(f"DEBUG: Attempting to play URL: {url}")
            
            # Tenta primeiro com from_probe
            try:
                source = await discord.FFmpegOpusAudio.from_probe(
                    url,
                    executable=FFMPEG_EXECUTABLE,
                    **FFMPEG_OPTIONS
                )
            except Exception as e:
                print(f"DEBUG: from_probe failed, trying from_url: {e}")
                source = await discord.FFmpegOpusAudio.from_url(
                    url,
                    executable=FFMPEG_EXECUTABLE,
                    **FFMPEG_OPTIONS
                )

            def after_play(error):
                if error:
                    print(f"ERROR: Erro na reprodução: {error}")
                
                # Lógica de loop
                if looping.get(ctx.guild.id) and now_playing.get(ctx.guild.id):
                    # Re-adiciona a música atual à fila se o loop estiver ativo
                    current_song_info = {
                        'url': now_playing[ctx.guild.id]['url'],
                        'title': now_playing[ctx.guild.id]['title'],
                        'author': now_playing[ctx.guild.id]['requester'], # Mudar para o objeto author original se disponível
                        'duration': song_info['duration'] # Reusar a duração original da música
                    }
                    q.insert(0, current_song_info)
                
                # Usa create_task para evitar bloqueio
                asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

            # Para qualquer música que esteja tocando antes de começar a nova
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            ctx.voice_client.play(source, after=after_play)

            embed = discord.Embed(
                title="🎵 Tocando Agora",
                description=f"**[{title}]({url})**",
                color=0xE8E8E8
            )
            if duration:
                embed.add_field(name="⏱️ Duração", value=f"{duration//60}:{duration%60:02d}", inline=True)
                embed.add_field(name="👤 Pedido por", value=f"{author.name}", inline=True)
            embed.set_footer(text=f"👤 Pedido por: {author.name}", icon_url=author.avatar.url if author.avatar else None)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("🎧")

        except Exception as e:
            print(f"ERROR: Falha ao reproduzir {title}: {e}")
            await ctx.send(f"❌ Não foi possível reproduzir **{title}**: {e}")
            # Tenta a próxima música
            await self.play_next(ctx)

    @commands.command()
    async def testesom(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("❌ Você precisa estar em um canal de voz.")

        canal = ctx.author.voice.channel
        if not ctx.voice_client:
            await canal.connect()

        FFMPEG_EXECUTABLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ffmpeg.exe'))

        try:
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -b:a 192k'
            }
            print(f"DEBUG: Attempting to play test sound with FFmpeg: {FFMPEG_EXECUTABLE}")
            source = discord.FFmpegOpusAudio(
                "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav",
                executable=FFMPEG_EXECUTABLE,
                **FFMPEG_OPTIONS
            )
            ctx.voice_client.play(source)
            await ctx.send("🔊 Testando som...")
        except Exception as e:
            print(f"ERROR: Test sound failed: {e}")
            await ctx.send(f"❌ Erro ao testar som: {e}")

async def setup(bot):
    await bot.add_cog(Play(bot))

