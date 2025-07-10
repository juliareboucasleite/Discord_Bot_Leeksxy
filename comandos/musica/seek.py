import discord
from discord.ext import commands
from .utils import now_playing

class Seek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="seek", aliases=["irpara"])
    async def seek_command(self, ctx, position: str):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(
                title="❌ Nada Tocando",
                description="Não há nenhuma música tocando no momento para usar o comando de busca.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if not hasattr(vc.source, 'duration') or not vc.source.duration:
            embed = discord.Embed(
                title="❌ Indisponível",
                description="Não é possível buscar nesta música.",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        try:
            # Converte a posição para segundos (mm:ss ou ss)
            if ':' in position:
                minutes, seconds = map(int, position.split(':'))
                seek_time = minutes * 60 + seconds
            else:
                seek_time = int(position)

            if not (0 <= seek_time <= vc.source.duration):
                embed = discord.Embed(
                    title="⚠️ Posição Inválida",
                    description=f"Por favor, forneça uma posição entre 0 e {int(vc.source.duration)} segundos.",
                    color=0xFFD700
                )
                return await ctx.send(embed=embed)

            # A lógica para buscar uma posição específica em uma música em reprodução
            # com discord.FFmpegPCMAudio pode ser complexa e geralmente requer recriar o source.
            # Para simplicidade, vamos apenas informar que a funcionalidade não está disponível
            # ou simular um reinício da música a partir da posição.
            # A implementação real de seek em FFmpegPCMAudio não é direta.
            # Por exemplo, uma abordagem seria: vc.source = discord.FFmpegPCMAudio(audio_url, before_options=f'-ss {seek_time}')
            # Mas isso exigiria reobter o audio_url e as opções, o que é complicado sem acesso à fila.

            embed = discord.Embed(
                title="⚠️ Funcionalidade de Busca (Seek)",
                description="A funcionalidade de busca (seek) é complexa e requer uma refatoração mais profunda do sistema de música.",
                color=0xFFD700
            )
            embed.add_field(name="Próximos Passos", value="Por enquanto, o comando de busca (seek) não está totalmente implementado. Considere pular ou reiniciar a música.", inline=False)
            await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="❌ Formato Inválido",
                description="Por favor, use o formato `mm:ss` ou `ss` para a posição.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Seek(bot)) 