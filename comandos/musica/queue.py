import discord
from discord.ext import commands
from comandos.musica.play import queue, now_playing

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx, page: int = 1):
        vc = ctx.voice_client
        if not vc:
            return await ctx.send("❌ Não estou em um canal de voz.")

        q = queue.get(ctx.guild.id, [])
        musica_info = now_playing.get(ctx.guild.id)

        if not q and not musica_info:
            return await ctx.send("❌ A fila está vazia e nenhuma música está tocando.")

        # Calcula o número total de páginas
        songs_per_page = 10
        total_pages = (len(q) + songs_per_page - 1) // songs_per_page

        if page < 1 or page > total_pages:
            return await ctx.send(f"❌ Página inválida. Use um número entre 1 e {total_pages}.")

        embed = discord.Embed(
            title="📋 Fila de Músicas",
            description=f"Página **{page}** de **{total_pages}**",
            color=0xE8E8E8
        )

        # Adiciona informações sobre a música atual
        if musica_info:
            embed.add_field(
                name="🎵 Tocando Agora",
                value=f"[{musica_info['title']}]({musica_info['url']})",
                inline=False
            )

        # Adiciona informações sobre a fila
        if q:
            start_idx = (page - 1) * songs_per_page
            end_idx = min(start_idx + songs_per_page, len(q))
            current_page = q[start_idx:end_idx]

            queue_text = ""
            for i, song in enumerate(current_page, start_idx + 1):
                queue_text += f"**{i}.** [{song['title']}]({song['url']})\n"

            embed.add_field(
                name=f"⏭️ Próximas Músicas ({len(q)})",
                value=queue_text,
                inline=False
            )

            # Adiciona informações sobre o tempo total
            total_duration = sum(song.get('duration', 0) for song in q)
            hours = total_duration // 3600
            minutes = (total_duration % 3600) // 60
            seconds = total_duration % 60

            if hours > 0:
                duration_str = f"{hours}h {minutes}m {seconds}s"
            else:
                duration_str = f"{minutes}m {seconds}s"

            embed.add_field(
                name="⏱️ Duração Total",
                value=f"**{duration_str}**",
                inline=False
            )
        else:
            embed.add_field(
                name="📭 Fila",
                value="A fila está vazia.",
                inline=False
            )

        # Adiciona informações sobre os controles
        embed.add_field(
            name="🎮 Controles",
            value=(
                "`!play` - Adicionar música\n"
                "`!skip` - Pular música atual\n"
                "`!remove <número>` - Remover música\n"
                "`!clearqueue` - Limpar fila\n"
                "`!shuffle` - Embaralhar fila"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Queue(bot))