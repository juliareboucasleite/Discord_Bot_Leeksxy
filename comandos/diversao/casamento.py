import discord
from discord.ext import commands
import sqlite3
import asyncio

conn = sqlite3.connect("dados.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS casamento (
    user_id INTEGER PRIMARY KEY,
    parceiro_id INTEGER
)
""")
conn.commit()

class Casamento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="casamento", aliases=["casar", "namorar", "marry", "marriage", "propor"], help='Propõe casamento a um membro. Uso: \'casamento <@membro>')
    async def casamento(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()
        autor = ctx.author

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem casar?",
                description="Por favor, mencione alguém para propor casamento!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == autor.id:
            embed = discord.Embed(
                title="💔 Amor Próprio Demais?",
                description="Você não pode se casar consigo mesmo! Que tal encontrar outra pessoa?",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Casado(a)!",
                description="Desculpe, eu já sou casado(a) com a Juubi (é segredo!).",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed)

        # Verificar se já está casado
        c.execute("SELECT parceiro_id FROM casamento WHERE user_id = ?", (autor.id,))
        if c.fetchone():
            embed = discord.Embed(
                title="💍 Já Casado(a)!",
                description=f"{autor.mention}, você já está casado(a)!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        c.execute("SELECT parceiro_id FROM casamento WHERE user_id = ?", (membro.id,))
        if c.fetchone():
            embed = discord.Embed(
                title="💍 Membro Casado!",
                description=f"{membro.mention} já está casado(a) com outra pessoa!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        # Perguntar ao parceiro
        embed_proposal = discord.Embed(
            title="💖 Pedido de Casamento!",
            description=f"🔔 {membro.mention}, {autor.mention} está te pedindo em casamento! Você aceita?\nReaja com 💍 para aceitar em 60 segundos.",
            color=0xE8E8E8
        )
        msg = await ctx.send(embed=embed_proposal)
        await msg.add_reaction("💍")

        def check(reaction, user):
            return (
                user.id == membro.id
                and str(reaction.emoji) == "💍"
                and reaction.message.id == msg.id
            )

        try:
            await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError: # Use asyncio.TimeoutError para o timeout
            embed_timeout = discord.Embed(
                title="⌛ Tempo Esgotado!",
                description="O pedido de casamento expirou. Talvez na próxima!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed_timeout)

        # Registrar casamento
        c.execute("INSERT INTO casamento (user_id, parceiro_id) VALUES (?, ?)", (autor.id, membro.id))
        c.execute("INSERT INTO casamento (user_id, parceiro_id) VALUES (?, ?)", (membro.id, autor.id))
        conn.commit()

        embed_success = discord.Embed(
            title="💞 Casamento Realizado!",
            description=f"Que lindo! {autor.mention} e {membro.mention} agora estão casados! Felicidades ao novo casal!",
            color=0xE8E8E8
        )
        embed_success.set_thumbnail(url="https://media.giphy.com/media/xT39DP4N2p1D1i0qN2/giphy.gif") # Exemplo de gif de casamento
        embed_success.set_footer(text="Que o amor de vocês dure para sempre!")
        embed_success.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed_success)

async def setup(bot):
    await bot.add_cog(Casamento(bot))
