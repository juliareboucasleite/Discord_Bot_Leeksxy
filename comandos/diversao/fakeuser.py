from discord.ext import commands
import discord
from typing import Optional

class FakeUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fakeuser")
    async def fakeuser(self, ctx, user: Optional[discord.User] = None, *, fala: Optional[str] = None):
        await ctx.message.delete()
        if not user:
            await ctx.send("Mencione um usuário!")
            return
        if not fala:
            await ctx.send("Fale uma coisa!")
            return

        try:
            webhook = await ctx.channel.create_webhook(name=user.name, avatar=await user.avatar.read() if user.avatar else None)
            await webhook.send(fala, username=user.name, avatar_url=user.avatar.url if user.avatar else None)
            await webhook.delete()
        except Exception as e:
            await ctx.send(f"Erro ao criar fakeuser: {e}")

async def setup(bot):
    await bot.add_cog(FakeUser(bot))