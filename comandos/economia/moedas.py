import discord
import sqlite3
from discord.ext import commands
from contextlib import contextmanager

DATABASE = "dados.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    try:
        yield conn
    finally:
        conn.close()

def setup_database():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS user_economy (user_id INTEGER, guild_id INTEGER, balance INTEGER DEFAULT 0, last_work TEXT, PRIMARY KEY (user_id, guild_id))")
        conn.commit()

class Moedas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        setup_database()

    async def get_saldo(self, user_id, guild_id):
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT balance FROM user_economy WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
            result = c.fetchone()
            return result[0] if result else 0

    async def update_saldo(self, user_id, guild_id, amount):
        with get_db_connection() as conn:
            c = conn.cursor()
            current_saldo = await self.get_saldo(user_id, guild_id)
            new_saldo = current_saldo + amount
            if new_saldo < 0:  # Para evitar saldo negativo
                new_saldo = 0

            if current_saldo == 0 and amount > 0:  # Se o usuário não existe e estamos adicionando moedas
                c.execute("INSERT INTO user_economy (user_id, guild_id, balance) VALUES (?, ?, ?)", (user_id, guild_id, amount))
            else:
                c.execute("UPDATE user_economy SET balance = ? WHERE user_id = ? AND guild_id = ?", (new_saldo, user_id, guild_id))
            conn.commit()

    @commands.command(name="saldo", aliases=["moedas", "money", "balance"])
    async def show_saldo(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()
        target_user = membro or ctx.author
        saldo = await self.get_saldo(target_user.id, ctx.guild.id)

        embed = discord.Embed(
            title="💰 Saldo de Moedas",
            description=f"O saldo de **{target_user.display_name}** é de **{saldo} moedas**.",
            color=0xE8E8E8
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else None)
        embed.set_footer(text="Continue interagindo para ganhar mais moedas!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @commands.command(name="pay", aliases=["enviarmoedas", "transferir", "sendcoins", "transfercoins"])
    async def pay(self, ctx, membro: discord.Member = None, valor: int = None):
        await ctx.message.delete()

        if not membro or valor is None:
            embed = discord.Embed(
                title="❌ Argumentos Ausentes",
                description="Uso correto: `'pay <membro> <quantia>`",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if valor <= 0:
            embed = discord.Embed(
                title="❌ Valor Inválido",
                description="A quantia de moedas a ser enviada deve ser maior que zero.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="❌ Transferência Inválida",
                description="Você não pode enviar moedas para si mesmo.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)
        
        if membro.bot:
            embed = discord.Embed(
                title="❌ Transferência Inválida",
                description="Você não pode enviar moedas para um bot.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        sender_saldo = await self.get_saldo(ctx.author.id, ctx.guild.id)
        if sender_saldo < valor:
            embed = discord.Embed(
                title="💸 Saldo Insuficiente",
                description=f"Você não tem **{valor} moedas** para enviar. Seu saldo atual é **{sender_saldo}**.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        await self.update_saldo(ctx.author.id, ctx.guild.id, -valor)
        await self.update_saldo(membro.id, ctx.guild.id, valor)

        embed = discord.Embed(
            title="💸 Moedas Enviadas!",
            description=f"**{ctx.author.display_name}** enviou **{valor} moedas** para **{membro.display_name}**!",
            color=0xE8E8E8
        )
        embed.add_field(name="Remetente", value=ctx.author.mention, inline=True)
        embed.add_field(name="Destinatário", value=membro.mention, inline=True)
        embed.add_field(name="Quantia", value=f"**{valor} moedas**", inline=False)
        embed.set_footer(text=f"Novo saldo de {ctx.author.display_name}: {await self.get_saldo(ctx.author.id, ctx.guild.id)}")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @commands.command(name="addmoedas", aliases=["addcoins"])
    @commands.has_permissions(administrator=True)
    async def add_moedas(self, ctx, membro: discord.Member = None, valor: int = None):
        await ctx.message.delete()

        if not membro or valor is None:
            embed = discord.Embed(
                title="❌ Argumentos Ausentes",
                description="Uso correto: `'addmoedas <membro> <quantia>`",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if valor <= 0:
            embed = discord.Embed(
                title="❌ Valor Inválido",
                description="A quantia de moedas a ser adicionada deve ser maior que zero.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)
        
        await self.update_saldo(membro.id, ctx.guild.id, valor)

        embed = discord.Embed(
            title="💰 Moedas Adicionadas!",
            description=f"Foram adicionadas **{valor} moedas** ao saldo de **{membro.display_name}**.",
            color=0xE8E8E8
        )
        embed.add_field(name="Usuário", value=membro.mention, inline=True)
        embed.add_field(name="Quantia", value=f"**{valor} moedas**", inline=True)
        embed.set_footer(text=f"Novo saldo de {membro.display_name}: {await self.get_saldo(membro.id, ctx.guild.id)}")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @commands.command(name="removemoedas", aliases=["removecoins"])
    @commands.has_permissions(administrator=True)
    async def remove_moedas(self, ctx, membro: discord.Member = None, valor: int = None):
        await ctx.message.delete()

        if not membro or valor is None:
            embed = discord.Embed(
                title="❌ Argumentos Ausentes",
                description="Uso correto: `'removemoedas <membro> <quantia>`",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if valor <= 0:
            embed = discord.Embed(
                title="❌ Valor Inválido",
                description="A quantia de moedas a ser removida deve ser maior que zero.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)
        
        current_saldo = await self.get_saldo(membro.id, ctx.guild.id)
        if current_saldo < valor:  # Evita remover mais do que o usuário tem
            embed = discord.Embed(
                title="⚠️ Saldo Insuficiente",
                description=f"**{membro.display_name}** não tem **{valor} moedas** para remover. Saldo atual: **{current_saldo}**.",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        await self.update_saldo(membro.id, ctx.guild.id, -valor)

        embed = discord.Embed(
            title="💸 Moedas Removidas!",
            description=f"Foram removidas **{valor} moedas** do saldo de **{membro.display_name}**.",
            color=0xE8E8E8
        )
        embed.add_field(name="Usuário", value=membro.mention, inline=True)
        embed.add_field(name="Quantia", value=f"**{valor} moedas**", inline=True)
        embed.set_footer(text=f"Novo saldo de {membro.display_name}: {await self.get_saldo(membro.id, ctx.guild.id)}")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🚫 Permissões Insuficientes",
                description="Você não tem permissão para usar este comando.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="❌ Argumento Inválido",
                description="Por favor, forneça um valor numérico válido.",
                color=0xE8E8E8
            )
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moedas(bot))
