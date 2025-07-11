import discord
from discord.ext import commands
import os
from glob import glob

STAFF_GUILD_ID = int(os.getenv("STAFF_GUILD_ID", 0))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", 0))
BACKUP_CHANNEL_ID = int(os.getenv("BACKUP_CHANNEL_ID", 0))

class AdminPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="backup", help="Envia backup do banco e arquivos JSON para o canal de backup.")
    @commands.is_owner()
    async def backup(self, ctx):
        if ctx.guild and ctx.guild.id != STAFF_GUILD_ID:
            return await ctx.send("❌ Este comando só pode ser usado no servidor de staff do bot.")
        channel = self.bot.get_channel(BACKUP_CHANNEL_ID)
        if not channel:
            return await ctx.send("❌ Canal de backup não configurado.")
        files = [discord.File("dados.db")]
        for file in glob("data/*.json"):
            files.append(discord.File(file))
        await channel.send("Backup automático dos dados:", files=files)
        await ctx.send("✅ Backup enviado para o canal de backup!")

    @commands.command(name="reload", help="Recarrega um cog do bot.")
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            await self.bot.reload_extension(cog)
            await ctx.send(f"✅ Cog `{cog}` recarregado com sucesso!")
        except Exception as e:
            await ctx.send(f"❌ Erro ao recarregar `{cog}`: {e}")

    @commands.command(name="shutdown", help="Desliga o bot.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Desligando o bot...")
        await self.bot.close()

    @commands.command(name="log", help="Envia uma mensagem para o canal de log.")
    @commands.is_owner()
    async def log(self, ctx, *, mensagem: str):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return await ctx.send("❌ Canal de log não configurado.")
        await channel.send(f"[LOG MANUAL] {mensagem}")
        await ctx.send("✅ Log enviado!")

async def setup(bot):
    await bot.add_cog(AdminPanel(bot)) 