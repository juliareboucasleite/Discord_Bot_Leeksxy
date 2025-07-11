import discord
from discord.ext import commands
import re
from typing import Optional

class AddEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addemoji")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, emoji: Optional[str] = None, *, nome: Optional[str] = None):
        if not emoji:
            return await ctx.send("Por favor, diga qual emoji deseja adicionar.")

        custom_emoji_match = re.match(r"<a?:\w+:(\d+)>", emoji)
        
        if custom_emoji_match:
            emoji_id = custom_emoji_match.group(1)
            is_animated = emoji.startswith("<a:")
            emoji_name = nome or re.findall(r":(\w+):", emoji)[0]

            url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if is_animated else 'png'}"

            try:
                novo_emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=await self.download(url))
            except discord.Forbidden:
                return await ctx.send("❌ Não tenho permissão para adicionar emojis neste servidor.")
            except Exception as e:
                return await ctx.send(f"Erro ao adicionar emoji: {e}")

            embed = discord.Embed(
                title="✅ Emoji Adicionado",
                description=f"**Nome:** `{emoji_name}`\n[Visualizar emoji]({url})",
                color=discord.Color.random()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("📝 Esse é um emoji padrão do Discord, não precisa ser adicionado ao servidor.")

    async def download(self, url):
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.read()

def setup(bot):
    bot.add_cog(AddEmoji(bot))
