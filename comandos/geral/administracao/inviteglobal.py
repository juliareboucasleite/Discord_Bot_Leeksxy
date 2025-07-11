import discord
from discord.ext import commands

class InviteGlobal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="inviteglobal")
    async def inviteglobal(self, ctx, bot_id=None):
        if not bot_id:
            return await ctx.send("❗ Diga o ID do bot que você quer pegar o convite.")

        try:
            user = await self.bot.fetch_user(int(bot_id))
        except:
            return await ctx.send("❌ Bot não encontrado ou ID inválido.")

        invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=8"

        embed = discord.Embed(
            title=f"🔗 Link para adicionar o bot `{user}`:",
            description=f"[Clique aqui para adicionar.]({invite_url})",
            color=discord.Color.random()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(InviteGlobal(bot))
