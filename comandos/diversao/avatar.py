from discord.ext import commands
import discord

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="avatar",
        description="Mostra o avatar de um usuário",
        aliases=["av", "pfp", "fotoperfil", "perfil", "profile"]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()
        target_user = membro or ctx.author
        
        embed = discord.Embed(
            title=f"📸 Avatar de {target_user.display_name}",
            description=f"Aqui está o avatar de {target_user.mention}.",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        
        embed.set_image(url=target_user.avatar.url)
        embed.add_field(
            name="🔗 Link Direto",
            value=f"[Clique aqui para abrir a imagem]({target_user.avatar.url})",
            inline=False
        )
        
        embed.set_footer(text=f"ID: {target_user.id}")
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                title="❌ Membro Não Encontrado",
                description="Não consegui encontrar o membro que você mencionou.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.CommandOnCooldown):
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
    await bot.add_cog(Avatar(bot))
