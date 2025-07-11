import discord
from discord.ext import commands
from typing import Optional

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm", help="Envia uma DM para um usuário da guilda. Uso: dm <@usuário> <mensagem>")
    @commands.has_permissions(manage_messages=True)
    async def dm(self, ctx, member: Optional[discord.Member] = None, *, mensagem: Optional[str] = None):
        await ctx.message.delete()
        if not member:
            return await ctx.send("Você não mencionou um usuário ou forneceu uma identificação inválida.")
        if member.id == ctx.author.id:
            return await ctx.send("Você não pode enviar uma mensagem para si mesmo!")
        if member.id == ctx.guild.owner_id:
            return await ctx.send("Tentando burlar o sistema né? Não pode enviar DM para o dono do servidor!")
        if member.bot:
            return await ctx.send("Você não pode enviar mensagens para um bot!")
        if not mensagem:
            return await ctx.send("Você não especificou sua mensagem.")
        try:
            await member.send(mensagem)
            await ctx.send(f"Enviou uma mensagem para {member.display_name}.")
        except Exception:
            await ctx.send("Não posso enviar mensagens na DM desse usuário!")

def setup(bot):
    bot.add_cog(DM(bot))