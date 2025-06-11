import discord
from discord.ext import commands

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def musica(self, ctx):
        embed = discord.Embed(
            title="🎵 Comandos de Música",
            description="Aqui estão todos os comandos de música disponíveis. Lembre-se, o bot funciona melhor com **nomes ou links do YouTube**.",
            color=0xE8E8E8
        )

        embed.add_field(
            name="▶️ Reprodução",
            value=(
                "`'play <nome/link>` - Toca uma música ou adiciona à fila.\n"
                "`'pause` - Pausa a música atual.\n"
                "`'resume` - Retoma a música pausada.\n"
                "`'skip` - Pula para a próxima música na fila.\n"
                "`'stop` - Para a reprodução e limpa a fila.\n"
                "`'leave` - Desconecta o bot do canal de voz."
            ),
            inline=False
        )

        embed.add_field(
            name="🎚️ Controle",
            value=(
                "`'volume <0-200>` - Ajusta o volume da música.\n"
                "`'loop` - Ativa ou desativa o loop da música atual.\n"
                "`'shuffle` - Embaralha as músicas na fila.\n"
                "`'remove <número>` - Remove uma música específica da fila.\n"
                "`'seek <segundos>` - Avança ou retrocede na música atual."
            ),
            inline=False
        )

        embed.add_field(
            name="📋 Informações",
            value=(
                "`'nowplaying` - Mostra a música que está tocando agora.\n"
                "`'queue` - Exibe a fila de músicas.\n"
                "`'lyrics <nome da música>` - Busca a letra de uma música.\n"
                "`'painel` - Mostra um painel de controle com informações e atalhos."
            ),
            inline=False
        )

        embed.add_field(
            name="⭐ Favoritos & Histórico",
            value=(
                "`'favoritar` - Adiciona a música atual aos seus favoritos.\n"
                "`'favoritos` - Lista suas músicas favoritas.\n"
                "`'desfavoritar <número>` - Remove uma música dos seus favoritos.\n"
                "`'history` - Mostra seu histórico de músicas tocadas.\n"
                "`'clearhistory` - Limpa seu histórico de músicas."
            ),
            inline=False
        )
        
        embed.set_footer(text="Para melhor experiência, use links do YouTube ou nomes de músicas precisos.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Musica(bot)) 