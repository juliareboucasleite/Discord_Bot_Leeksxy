import discord
from discord.ext import commands
import random

class Kiss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kiss", aliases=["beijar", "beijo"], help='Dá um beijo em um membro. Uso: \'kiss <@membro>')
    async def kiss(self, ctx, membro: discord.Member = None):
        await ctx.message.delete()

        gifs = [
            'https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865',
            'https://i.pinimg.com/originals/7e/28/71/7e28715f3c114dc720688f1a03abc5f5.gif',
            'https://imgur.com/w1TU5mR.gif',
            'https://media.tenor.com/images/15053158c89b708298717904085b46e3/tenor.gif',
            'https://media.tenor.com/images/2237d1d2c67f08b3e8c9b9b4d4b1a4a5/tenor.gif'
        ]

        if not membro:
            embed = discord.Embed(
                title="🤔 Quem beijar?",
                description="Por favor, mencione um membro para beijar!",
                color=0xE8E8E8
            )
            return await ctx.send(embed=embed, ephemeral=True)

        if membro.id == self.bot.user.id:
            embed = discord.Embed(
                title="😳 Opa!",
                description="Você quer me beijar? Awn, que fofo, mas não rola! Sou um bot!",
                color=0xE8E8E8
            )
            embed.set_image(url=random.choice(gifs))
            return await ctx.send(embed=embed)

        if membro.id == ctx.author.id:
            embed = discord.Embed(
                title="🪞 Beijando a Si Mesmo?",
                description="Você se beijou no espelho... é um amor próprio e tanto!",
                color=0xE8E8E8
            )
            embed.set_image(url=random.choice(gifs))
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="💋 Beijo no Ar!",
            description=f"{ctx.author.mention} deu um beijo em {membro.mention}! Que fofos!",
            color=0xE8E8E8
        )
        embed.set_image(url=random.choice(gifs))
        
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_footer(text="Que o amor esteja no ar!")
        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Kiss(bot))
