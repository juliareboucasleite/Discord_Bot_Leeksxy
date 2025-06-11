import discord
import sqlite3
from discord.ext import commands

conn = sqlite3.connect("dados.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    nivel INTEGER DEFAULT 1
)""")
conn.commit()

class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="perfil", aliases=["profile"])
    async def show_perfil(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()
        target_user = membro or ctx.author

        # Buscar dados de XP e Nível
        c.execute("SELECT xp, nivel FROM usuarios WHERE user_id = ?", (target_user.id,))
        xp_data = c.fetchone()
        
        xp_atual, nivel_atual = (xp_data[0], xp_data[1]) if xp_data else (0, 1) # Default se não houver dados

        # Buscar saldo de moedas da tabela correta
        c.execute("SELECT balance FROM user_economy WHERE user_id = ? AND guild_id = ?", (target_user.id, ctx.guild.id))
        moedas_data = c.fetchone()
        saldo_moedas = moedas_data[0] if moedas_data else 0

        # Buscar status de casamento
        c.execute("SELECT parceiro_id FROM casamento WHERE user_id = ?", (target_user.id,))
        casamento_data = c.fetchone()
        
        casado_com = None
        if casamento_data:
            parceiro_id = casamento_data[0]
            parceiro = await self.bot.fetch_user(parceiro_id) # Buscar o objeto do parceiro
            if parceiro:
                casado_com = parceiro.mention
            else:
                casado_com = "Usuário desconhecido"

        # Calcular progresso de XP para a barra
        xp_necessario_proximo_nivel = nivel_atual * 100
        if xp_necessario_proximo_nivel == 0: # Evitar divisão por zero para nível 0 ou 1 recém-criado
            porcentagem_progresso = 0
        else:
            porcentagem_progresso = (xp_atual / xp_necessario_proximo_nivel) * 100
            if porcentagem_progresso > 100: # Se por algum motivo o XP exceder o necessário
                porcentagem_progresso = 100

        blocos_preenchidos = int(porcentagem_progresso // 10)
        blocos_vazios = 10 - blocos_preenchidos
        barra_progresso = "█" * blocos_preenchidos + "░" * blocos_vazios

        embed = discord.Embed(
            title=f"📋 Perfil de {target_user.display_name}",
            description=f"Informações de perfil para {target_user.mention}",
            color=0xE8E8E8 # Cor cinza claro para consistência
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
        
        # Informações de XP e Nível
        embed.add_field(
            name="🌟 Nível",
            value=f"**{nivel_atual}**",
            inline=True
        )
        embed.add_field(
            name="✨ XP Atual",
            value=f"**{xp_atual}**",
            inline=True
        )
        embed.add_field(
            name="➡️ Próximo Nível",
            value=f"**{xp_necessario_proximo_nivel - xp_atual} XP** restantes para o Nível {nivel_atual + 1}",
            inline=False
        )
        embed.add_field(name="Progresso", value=f"`{barra_progresso}` {porcentagem_progresso:.1f}%", inline=False)

        # Informações de Moedas
        embed.add_field(
            name="💰 Moedas",
            value=f"**{saldo_moedas} moedas**",
            inline=False
        )

        # Informações de Casamento
        if casado_com:
            embed.add_field(
                name="💖 Casado(a) com",
                value=casado_com,
                inline=False
            )
        else:
            embed.add_field(
                name="💖 Status de Casamento",
                value="Solteiro(a)",
                inline=False
            )

        # Outras informações do usuário
        embed.add_field(
            name="🆔 ID do Usuário",
            value=f"`{target_user.id}`",
            inline=True
        )
        embed.add_field(
            name="🗓️ Entrou no Discord",
            value=f"<t:{int(target_user.created_at.timestamp())}:D> (<t:{int(target_user.created_at.timestamp())}:R>)",
            inline=True
        )
        embed.add_field(
            name="🗓️ Entrou no Servidor",
            value=f"<t:{int(target_user.joined_at.timestamp())}:D> (<t:{int(target_user.joined_at.timestamp())}:R>)",
            inline=True
        )

        embed.set_footer(text="Informações do perfil")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Perfil(bot))
