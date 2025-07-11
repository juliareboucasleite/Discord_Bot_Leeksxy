import discord
from discord.ext import commands
from comandos.musica.musica import queue
from comandos.musica.utils import now_playing
from utils.pagination_py import paginate

class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def queue(self, ctx):
        vc = ctx.voice_client
        if not vc:
            return await ctx.send("❌ Não estou em um canal de voz.")

        q = queue.get(ctx.guild.id, [])
        musica_info = now_playing.get(ctx.guild.id)

        if not q and not musica_info:
            return await ctx.send("❌ A fila está vazia e nenhuma música está tocando.")

        songs_per_page = 10
        pages = []

        # Cria as páginas de embed
        for page_num in range(0, len(q), songs_per_page):
            embed = discord.Embed(
                title="📋 Fila de Músicas",
                color=0xE8E8E8
            )
            if musica_info and page_num == 0:
                embed.add_field(
                    name="🎵 Tocando Agora",
                    value=f"[{musica_info['title']}]({musica_info['url']})",
                    inline=False
                )
            current_page = q[page_num:page_num + songs_per_page]
            queue_text = ""
            for i, song in enumerate(current_page, page_num + 1):
                queue_text += f"**{i}.** [{song['title']}]({song['url']})\n"
            embed.add_field(
                name=f"⏭️ Próximas Músicas ({len(q)})",
                value=queue_text if queue_text else "A fila está vazia.",
                inline=False
            )
            pages.append(embed)

        # Usa a paginação por reações
        await paginate(ctx, pages)

async def setup(bot):
    await bot.add_cog(Queue(bot))