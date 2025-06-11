import discord
from discord.ext import commands
from .utils import now_playing

class Volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def volume(self, ctx, volume: int = None):
        vc = ctx.voice_client
        if not vc:
            return await ctx.send("❌ Não estou em um canal de voz.")

        if volume is None:
            # Mostra o volume atual
            current_volume = int(vc.source.volume * 100) if vc.source else 100
            musica_info = now_playing.get(ctx.guild.id)

            embed = discord.Embed(
                title="🔊 Volume Atual",
                description=f"O volume atual é **{current_volume}%**",
                color=0xE8E8E8
            )

            if musica_info:
                embed.add_field(
                    name="🎵 Música Atual",
                    value=f"[{musica_info['title']}]({musica_info['url']})",
                    inline=False
                )

            # Adiciona uma barra visual do volume
            volume_bar = "█" * (current_volume // 10) + "░" * (10 - (current_volume // 10))
            embed.add_field(
                name="Volume",
                value=f"`{volume_bar}` {current_volume}%",
                inline=False
            )

            await ctx.send(embed=embed)
            return

        if not 0 <= volume <= 200:
            return await ctx.send("❌ O volume deve estar entre 0 e 200%.")

        vc.source.volume = volume / 100
        musica_info = now_playing.get(ctx.guild.id)

        embed = discord.Embed(
            title="🔊 Volume Alterado",
            description=f"Volume alterado para **{volume}%**",
            color=0xE8E8E8
        )

        if musica_info:
            embed.add_field(
                name="🎵 Música Atual",
                value=f"[{musica_info['title']}]({musica_info['url']})",
                inline=False
            )

        # Adiciona uma barra visual do volume
        volume_bar = "█" * (volume // 10) + "░" * (10 - (volume // 10))
        embed.add_field(
            name="Volume",
            value=f"`{volume_bar}` {volume}%",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Volume(bot))
