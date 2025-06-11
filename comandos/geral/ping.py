from discord.ext import commands
import discord

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ping",
        description="Mostra a latência do bot",
        aliases=["latency"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(
            title="🏓 Pong!",
            description="Verificando a latência do bot...",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text="Leeksxy - Latência")
        embed.timestamp = discord.utils.utcnow()

        initial_msg = await ctx.send(embed=embed)

        # Calcula a latência da API (roundtrip latency)
        api_latency = round(self.bot.latency * 1000)

        # Calcula a latência da mensagem (tempo entre o envio e a edição)
        message_latency = round((initial_msg.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000)

        embed.description = "Latência calculada!"
        embed.add_field(
            name="📡 Latência do WebSocket",
            value=f"**{api_latency}ms**",
            inline=True
        )
        embed.add_field(
            name="✉️ Latência da Mensagem",
            value=f"**{message_latency}ms**",
            inline=True
        )
        
        await initial_msg.edit(embed=embed)

    @ping.error
    async def ping_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Comando em Espera",
                description=f"Por favor, aguarde **{error.retry_after:.1f} segundos** para usar este comando novamente.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="⚠️ Erro Desconhecido",
                description=f"Ocorreu um erro ao executar o comando: `{error}`",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ping(bot))