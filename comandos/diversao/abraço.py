import discord
from discord.ext import commands
import aiohttp
import random
from typing import Optional

class Abraco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="abraco", aliases=["abraço", "hug", "abracar", "abraçar"])
    async def abracar_command(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
         'https://media.discordapp.net/attachments/733751317041905745/736632457578676254/hug.gif?width=426&height=395',
          'https://media.discordapp.net/attachments/733751317041905745/736632470820225064/hug4.gif?width=198&height=134',
          'https://media.discordapp.net/attachments/733751317041905745/736632483575103498/hug5.gif?width=198&height=175',
          'https://media.discordapp.net/attachments/733751317041905745/736632488025129000/hug7.gif?width=198&height=124',
          'https://media.discordapp.net/attachments/733751317041905745/736632515544219722/hug2.gif?width=379&height=395',
         'https://media.discordapp.net/attachments/733751317041905745/736632518727696464/hug8.gif?width=450&height=251',
         'https://media.discordapp.net/attachments/733751317041905745/736632544526860388/hug6.gif?width=450&height=227',
         'https://media.discordapp.net/attachments/733751317041905745/736632554005856286/hug3.gif?width=448&height=250',
         'https://media.discordapp.net/attachments/733751317041905745/736632565309505596/hug1.gif?width=448&height=250'
        ]

        # Tenta pegar GIF da API waifu.pics
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.waifu.pics/sfw/hug") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        gif_url = data["url"]
                    else:
                        gif_url = random.choice(gifs)
        except Exception:
            gif_url = random.choice(gifs)

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem abraçar?",
                description="Por favor, mencione um membro para dar um abraço!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😊 Awn, obrigado!",
                description="Obrigado por me abraçar! Fico feliz em receber carinho!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🙃 Auto Abraço",
                description="Você se abraçou sozinho... É fofo e um pouco triste ao mesmo tempo!",
                color=0xE8E8E8
            )
            embed.set_image(url=gif_url)
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="🤗 Abraço Recebido!",
            description=f"{ctx.author.mention} deu um abraço apertado em {membro.mention}!",
            color=0xE8E8E8
        )
        embed.set_image(url=gif_url)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Sinta o carinho!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Abraco(bot))
