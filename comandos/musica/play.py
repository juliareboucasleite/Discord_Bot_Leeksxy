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

def get_ffmpeg_path():
    # Try to find ffmpeg in the current directory first
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ffmpeg_path = os.path.join(current_dir, 'ffmpeg.exe')
    
    if os.path.exists(ffmpeg_path):
        return ffmpeg_path
    
    # If not found, try to use system ffmpeg
    return 'ffmpeg'

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.FFMPEG_EXECUTABLE = get_ffmpeg_path()
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -b:a 320k'  # Increased bitrate for better quality
        }
        self.YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'extract_flat': False,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

    @commands.command()
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Você precisa estar em um canal de voz para usar este comando.")

        channel = ctx.author.voice.channel
        
        if not channel.permissions_for(ctx.guild.me).connect:
            return await ctx.send("❌ Não tenho permissão para entrar no canal de voz. Por favor, verifique as permissões do bot.")
        if not channel.permissions_for(ctx.guild.me).speak:
            return await ctx.send("❌ Não tenho permissão para falar no canal de voz. Por favor, verifique as permissões do bot.")

        try:
            if not ctx.voice_client:
                await channel.connect()
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
        except Exception as e:
            return await ctx.send(f"❌ Erro ao conectar ao canal de voz: {str(e)}")

        async with ctx.typing():
            try:
                with yt_dlp.YoutubeDL(self.YTDL_OPTIONS) as ydl:
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
                        return await ctx.send("❌ Não foi possível encontrar uma fonte de áudio válida para sua busca.")

                    title = info.get('title', 'Título desconhecido')
                    duration = info.get('duration', 0)
                    
                    q = get_queue(ctx.guild.id)
                    q.append({
                        'url': url,
                        'title': title,
                        'author': ctx.author,
                        'duration': duration,
                        'thumbnail': info.get('thumbnail')
                    })

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
                        if info.get('thumbnail'):
                            embed.set_thumbnail(url=info['thumbnail'])
                        embed.set_footer(text=f"Posição na fila: {len(q)}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
                        await ctx.send(embed=embed)

            except Exception as e:
                error_msg = str(e)
                if "Video unavailable" in error_msg:
                    await ctx.send("❌ Este vídeo não está disponível ou é privado.")
                elif "Sign in" in error_msg:
                    await ctx.send("❌ Este vídeo requer login para ser acessado.")
                else:
                    await ctx.send(f"❌ Ocorreu um erro ao processar sua solicitação: {error_msg}")
                print(f"ERROR: Play command error: {e}")

    async def play_next(self, ctx):
        q = get_queue(ctx.guild.id)
        if not q:
            await ctx.send("✅ Fila finalizada. O bot permanecerá no canal.")
            now_playing[ctx.guild.id] = {'title': 'Nenhuma música tocando', 'url': None, 'requester': None}
            looping[ctx.guild.id] = False
            return

        song_info = q.pop(0)
        url = song_info['url']
        title = song_info['title']
        author = song_info['author']
        duration = song_info['duration']
        thumbnail = song_info.get('thumbnail')

        now_playing[ctx.guild.id] = {'title': title, 'url': url, 'requester': author.display_name}

        # Save to history
        try:
            conn = sqlite3.connect('dados.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO history (guild_id, user_id, title, url)
                VALUES (?, ?, ?, ?)
            ''', (ctx.guild.id, author.id, title, url))
            conn.commit()
        except Exception as e:
            print(f"ERROR: Failed to save to history: {e}")
        finally:
            conn.close()

        try:
            source = await discord.FFmpegOpusAudio.from_probe(
                url,
                executable=self.FFMPEG_EXECUTABLE,
                **self.FFMPEG_OPTIONS
            )

            def after_play(error):
                if error:
                    print(f"ERROR: Playback error: {error}")
                
                if looping.get(ctx.guild.id) and now_playing.get(ctx.guild.id):
                    current_song_info = {
                        'url': now_playing[ctx.guild.id]['url'],
                        'title': now_playing[ctx.guild.id]['title'],
                        'author': now_playing[ctx.guild.id]['requester'],
                        'duration': duration,
                        'thumbnail': thumbnail
                    }
                    q.insert(0, current_song_info)
                
                asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

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
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text=f"Músicas na fila: {len(q)}", icon_url=author.avatar.url if author.avatar else None)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("🎧")

        except Exception as e:
            print(f"ERROR: Failed to play {title}: {e}")
            await ctx.send(f"❌ Não foi possível reproduzir **{title}**: {str(e)}")
            await self.play_next(ctx)

    @commands.command()
    async def testesom(self, ctx):
        if not ctx.author.voice:
            return await ctx.send("❌ Você precisa estar em um canal de voz para usar este comando.")

        canal = ctx.author.voice.channel
        if not ctx.voice_client:
            await canal.connect()

        try:
            source = discord.FFmpegOpusAudio(
                "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars60.wav",
                executable=self.FFMPEG_EXECUTABLE,
                **self.FFMPEG_OPTIONS
            )
            ctx.voice_client.play(source)
            await ctx.send("🔊 Testando som...")
        except Exception as e:
            await ctx.send(f"❌ Erro ao testar som: {str(e)}")

async def setup(bot):
    await bot.add_cog(Play(bot))

