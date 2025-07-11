import discord
from discord.ext import commands
import random
from typing import Optional

class Kiss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kiss", aliases=["beijar", "beijo"], help='Dá um beijo em um membro. Uso: \'kiss <@membro>')
    async def kiss(self, ctx, membro: Optional[discord.Member] = None):
        await ctx.message.delete()

        gifs = [
            'https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865',
            'https://i.pinimg.com/originals/7e/28/71/7e28715f3c114dc720688f1a03abc5f5.gif',
            'https://imgur.com/w1TU5mR.gif',
            'https://media.tenor.com/images/15053158c89b708298717904085b46e3/tenor.gif',
            'https://media.tenor.com/images/2237d1d2c67f08b3e8c9b9b4d4b1a4a5/tenor.gif'
            'https://cdn.discordapp.com/attachments/1323396556933697678/1392594066335858910/dd277ba78ad859a4.gif?ex=6872140a&is=6870c28a&hm=38be34abd570095dfeb7996acc57937aa51bd403b24797eee0a96ae4edcd3828&',
            'https://rrp-production.loritta.website/img/dfa3f0d6173bd4a831fbef1b0f592e683e8bfb0c.gif',
            'https://cdn.nekotina.com/images/FS2OFASQ.gif',
            'https://cdn.nekotina.com/images/3BP3R3ml.gif',
            'https://cdn.discordapp.com/attachments/1323396556933697678/1381009307729920181/d1fcea8c9b64bf50.gif?ex=68721ee4&is=6870cd64&hm=78f2472dfb262b8c8179e7c5a918b9a182bcda357f31bd98e6571871d23d13f4&',
            'https://cdn.discordapp.com/attachments/1323396556933697678/1381093394884984972/a3eef49db396b317.gif?ex=6871c474&is=687072f4&hm=3953acdbc0df37c67c6231e816b8f49a98bbb42015a47845d58470b7a956923f&',
            'https://cdn.nekotina.com/images/G_nzi8VM.gif'
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
