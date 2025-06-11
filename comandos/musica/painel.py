import discord
from discord.ext import commands
from .utils import now_playing, looping
from comandos.musica.play import queue

class MusicControlView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="⏯️ Pause/Resume", style=discord.ButtonStyle.primary, custom_id="painel_play_pause")
    async def pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            if vc.is_paused():
                await interaction.response.send_message("▶️ Música retomada.", ephemeral=True)
                await self.bot.get_command("resume").invoke(await self.bot.get_context(interaction))
            elif vc.is_playing():
                await interaction.response.send_message("⏸️ Música pausada.", ephemeral=True)
                await self.bot.get_command("pause").invoke(await self.bot.get_context(interaction))
            else:
                await interaction.response.send_message("❌ Nada está tocando.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Bot não está no canal de voz.", ephemeral=True)

    @discord.ui.button(label="⏭️ Pular", style=discord.ButtonStyle.success, custom_id="painel_skip")
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            await interaction.response.send_message("⏭️ Música pulada.", ephemeral=True)
            await self.bot.get_command("skip").invoke(await self.bot.get_context(interaction))
        else:
            await interaction.response.send_message("❌ Nada está tocando.", ephemeral=True)

    @discord.ui.button(label="⏹️ Parar", style=discord.ButtonStyle.danger, custom_id="painel_stop")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            await interaction.response.send_message("⏹️ Música parada e saí do canal.", ephemeral=True)
            await self.bot.get_command("stop").invoke(await self.bot.get_context(interaction))
        else:
            await interaction.response.send_message("❌ Bot não está no canal de voz.", ephemeral=True)

    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.secondary, custom_id="painel_loop")
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            # Chamar o comando de loop
            await interaction.response.send_message("🔄 Trocando estado do loop...", ephemeral=True)
            await self.bot.get_command("loop").invoke(await self.bot.get_context(interaction))
        else:
            await interaction.response.send_message("❌ Bot não está no canal de voz.", ephemeral=True)

    @discord.ui.button(label="👋 Sair", style=discord.ButtonStyle.red, custom_id="painel_leave")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            await interaction.response.send_message("👋 Saindo do canal de voz...", ephemeral=True)
            await self.bot.get_command("leave").invoke(await self.bot.get_context(interaction))
        else:
            await interaction.response.send_message("❌ Bot não está no canal de voz.", ephemeral=True)

class Painel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="painel", aliases=["mpanel", "musicpanel"])
    async def painel_command(self, ctx):
        vc = ctx.guild.voice_client
        q = queue.get(ctx.guild.id, [])

        # Embed principal de status
        embed = discord.Embed(
            title="🎶 Painel de Música",
            description="Controle a reprodução de música aqui.",
            color=0xE8E8E8
        )

        # Status da música atual
        current_song_info = now_playing.get(ctx.guild.id, {})
        music_title = current_song_info.get('title')
        music_url = current_song_info.get('url')
        requester = current_song_info.get('requester')

        if music_title and music_url and (vc.is_playing() or vc.is_paused()):
            status_text = f"**Tocando:** [{music_title}]({music_url})\nPedida por: {requester if requester else 'Desconhecido'}"
            if vc.is_paused():
                status_text += " (Pausado)"
        else:
            status_text = "Nenhuma música tocando no momento."
        embed.add_field(name="🎵 Status Atual", value=status_text, inline=False)

        # Fila
        if q:
            next_songs = "\n".join([f"• [{song['title']}]({song['url']})" for song in q[:5]])
            embed.add_field(name=f"⏭️ Próximas na Fila ({len(q)} músicas)", value=next_songs + ("\n..." if len(q) > 5 else ""), inline=False)
        else:
            embed.add_field(name="📭 Fila", value="A fila está vazia.", inline=False)

        # Loop
        loop_status = "Ativado" if looping.get(ctx.guild.id, False) else "Desativado"
        embed.add_field(name="🔁 Loop", value=loop_status, inline=True)
        
        # Volume (Se disponível, pois o source pode não ter volume_level)
        if vc.source and hasattr(vc.source, 'volume') and vc.source.volume is not None:
            volume_percent = int(vc.source.volume * 100)
            embed.add_field(name="🔊 Volume", value=f"{volume_percent}%", inline=True)

        # Adicionar botões de controle
        view = MusicControlView(self.bot)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Painel(bot))

