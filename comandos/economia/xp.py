import sqlite3
import discord
from discord.ext import commands

conn = sqlite3.connect("dados.db")
c = conn.cursor()

# Criar a tabela 'usuarios' se não existir
c.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    nivel INTEGER DEFAULT 1
)
""")
conn.commit()

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.adicionar_xp, "on_message")

    async def adicionar_xp(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id
        guild_id = message.guild.id # Adicionado para garantir XP por servidor, se necessário
        
        # Para este exemplo, vamos manter XP globalmente para simplicidade com a tabela atual
        # Se você quiser XP por servidor, a tabela precisaria de 'guild_id' como parte da PK
        
        c.execute("SELECT xp, nivel FROM usuarios WHERE user_id = ?", (user_id,))
        result = c.fetchone()

        if result:
            xp, nivel = result
            xp += 10 # XP por mensagem
            
            xp_para_proximo_nivel = nivel * 100
            if xp >= xp_para_proximo_nivel:
                xp = xp - xp_para_proximo_nivel # Reinicia XP para o próximo nível
                nivel += 1
                
                embed = discord.Embed(
                    title="🎉 Nível Subido! 🎉",
                    description=f"{message.author.mention} subiu para o **Nível {nivel}**!",
                    color=0xE8E8E8
                )
                embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
                embed.set_footer(text="Parabéns! Continue interagindo para subir de nível!")
                embed.timestamp = discord.utils.utcnow()
                await message.channel.send(embed=embed)

            c.execute("UPDATE usuarios SET xp = ?, nivel = ? WHERE user_id = ?", (xp, nivel, user_id))
        else:
            c.execute("INSERT INTO usuarios (user_id, xp, nivel) VALUES (?, ?, ?)", (user_id, 10, 1))
        conn.commit()

    @commands.command(name='xp', aliases=['level', 'rank', 'progresso', 'experiencia', 'nivel', 'levelup'], help='Mostra seu nível e progresso de XP.')
    @commands.bot_has_permissions(send_messages=True)
    async def xp_command(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()
        target_user = membro or ctx.author

        c.execute("SELECT xp, nivel FROM usuarios WHERE user_id = ?", (target_user.id,))
        result = c.fetchone()

        if not result:
            embed = discord.Embed(
                title="📊 Progresso de XP",
                description=f"{target_user.mention} ainda não tem XP registrado. Comece a interagir!",
                color=0xE8E8E8
            )
            if target_user.id == self.bot.user.id:
                embed.description = "Como um bot, eu não tenho XP ou níveis. Minha missão é te ajudar!"
            elif target_user.id == ctx.author.id:
                embed.description = "Você ainda não tem XP registrado. Comece a interagir no servidor para ganhar XP!"
            
            embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
            embed.set_footer(text="Vamos lá! ✨")
            embed.timestamp = discord.utils.utcnow()
            return await ctx.send(embed=embed, ephemeral=True)

        xp_atual, nivel_atual = result
        xp_necessario_proximo_nivel = nivel_atual * 100
        xp_restante = xp_necessario_proximo_nivel - xp_atual

        # Calcular porcentagem de progresso para a barra
        porcentagem_progresso = (xp_atual / xp_necessario_proximo_nivel) * 100
        blocos_preenchidos = int(porcentagem_progresso // 10)
        blocos_vazios = 10 - blocos_preenchidos
        barra_progresso = "█" * blocos_preenchidos + "░" * blocos_vazios

        embed = discord.Embed(
            title="📊 Progresso de XP",
            description=f"Informações de XP para {target_user.mention}",
            color=0xE8E8E8
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)

        embed.add_field(name="🌟 Nível", value=f"**{nivel_atual}**", inline=True)
        embed.add_field(name="✨ XP Atual", value=f"**{xp_atual}**", inline=True)
        embed.add_field(name="➡️ Próximo Nível", value=f"**{xp_restante} XP** restantes para o Nível {nivel_atual + 1}", inline=False)
        embed.add_field(name="Progresso", value=f"`{barra_progresso}` {porcentagem_progresso:.1f}%", inline=False)

        embed.set_footer(text="Continue interagindo para subir de nível!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(XP(bot))
