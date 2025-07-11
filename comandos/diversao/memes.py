import discord
from discord.ext import commands
import random
from datetime import datetime

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme", aliases=["memes", "zueira", "zueiras"])
    async def meme(self, ctx):
        memes = [
      'https://i.pinimg.com/236x/9a/d8/ac/9ad8accb00b77668c167e732e7eee086.jpg',
			'https://i.pinimg.com/originals/59/26/4f/59264f7c249e7aed2e9fdd5e16a15b7c.jpg',
			'https://pm1.narvii.com/6754/9f71519c6be50a0498e6026e7b99885540361cb4v2_hq.jpg',
			'https://images7.memedroid.com/images/UPLOADED806/594fef43aead3.jpeg',
			'https://i.redd.it/pml61y921av41.png',
			'https://imageproxy.ifunny.co/crop:x-20,resize:320x,crop:x800,quality:90x75/images/f1864c6767981423e05ef3184fa15b40eea4c2faa34e5fecbcac56528e9b951f_1.jpg',
      'https://i.pinimg.com/474x/04/c2/9c/04c29cf7a83bc4921bcfac0a9a879ffc.jpg',
      'https://i.ytimg.com/vi/XwMw6CzpJfw/maxresdefault.jpg',
      'https://scontent.fgru5-1.fna.fbcdn.net/v/t1.0-0/p526x296/120832834_645484016396761_7972813683411843819_n.jpg?_nc_cat=101&_nc_sid=825194&_nc_ohc=Pg_Dqm_U1R4AX-4OSuP&_nc_ht=scontent.fgru5-1.fna&tp=6&oh=1ee17fcaa11e781586d672f50b07f657&oe=5F9FD7FB',
      'https://i.pinimg.com/236x/e9/77/01/e977012b55273c6ee7af41debff83887.jpg',
      'https://d3q93wnyp4lkf8.cloudfront.net/revista/post_images/29272/086ec5bcf367dc06f82318eee018e68040ce3a62.png?1589228004',
      'https://amazonasatual.com.br/wp-content/uploads/2020/01/meme7-Copia-426x437.jpg',
      'https://m.leiaja.com/sites/default/files/field/image/negocios/2020/05/WhatsApp%20Image%202020-05-11%20at%2012.45.45%20%281%29.jpeg',
      'https://d3q93wnyp4lkf8.cloudfront.net/revista/post_images/29277/8f0072162de574df8f015681467b40274c0a3122.png?1589228385',
      'https://i.pinimg.com/236x/81/a1/14/81a1147fb0af970e2b11cff143d59d04.jpg',
      'https://i.pinimg.com/originals/9a/6e/23/9a6e23e04d50766561c097ae43a3d320.jpg',
      'https://i.pinimg.com/originals/f2/ec/3a/f2ec3aee083a28fa9566adacc209fd21.jpg',
      'https://i.pinimg.com/originals/17/6e/a4/176ea4d9384697191d1274792f3499c1.png',
      'https://img.r7.com/images/meme-terceira-guerra-03012020103903545',
      'https://www.portaltucuma.com.br/wp-content/uploads/2020/02/Manu-1024x778.png',
      'https://www.folhadelondrina.com.br/img/Facebook/2980000/Surto-de-memes-no-pais-da-piada-pronta0298201600202003101829.jpg',
      'https://i.pinimg.com/736x/fc/0e/4b/fc0e4b426f1affa39e1b1950b0febdec.jpg',
      'https://i.pinimg.com/236x/22/74/22/227422e5942c87bad5f09a9567613839.jpg',
      'https://i.pinimg.com/236x/69/a5/34/69a534b8a140e9fa7f3665407514eaa3.jpg',
      'https://i.pinimg.com/236x/9d/c2/54/9dc254f5a588425592cb39f946b33fba.jpg',
      'https://i.pinimg.com/236x/2a/7d/de/2a7dded13b2a0ad70fe954a410cba584.jpg',
      'https://pbs.twimg.com/media/ENC6XzIXsAAy8Bd.jpg',
      'https://pm1.narvii.com/7482/0b52dd63a89431c343c417f697c16c52cbf1f050r1-1285-1262v2_00.jpg',
      'https://i.pinimg.com/236x/e9/59/d5/e959d505f75bedcbaeef90e18aaff8c2.jpg',
      'https://i.pinimg.com/236x/ab/d8/2d/abd82d5cebe25c7e7343dd7698ba1bf8.jpg',
      'https://scontent.fgru5-1.fna.fbcdn.net/v/t1.0-0/p526x296/106128706_1845499068949039_213101206405618430_o.jpg?_nc_cat=101&_nc_sid=8bfeb9&_nc_ohc=gQCnQ-xtkkAAX82En5l&_nc_ht=scontent.fgru5-1.fna&_nc_tp=6&oh=d0138d3cc5baa9cd278d0baee5858358&oe=5F55F95D',
      'https://scontent.fgru5-1.fna.fbcdn.net/v/t1.0-0/p180x540/117301592_1686293281522977_4176341516622659972_n.png?_nc_cat=1&_nc_sid=730e14&_nc_ohc=y3crS7GyPHEAX_2SXDq&_nc_ht=scontent.fgru5-1.fna&oh=0bd9340550a2a5b1945af414fc217e15&oe=5F532344w',
      'https://cdn.discordapp.com/attachments/724845889373601892/742158321301323786/unknown.png',
      'https://img.ibxk.com.br/ns/rexposta/2019/03/07/07104246573110.jpg?watermark=neaki&watermark=neaki',
      'https://imageproxy.ifunny.co/crop:x-20,resize:320x,crop:x800,quality:90x75/images/32d07ceef9a3561633280aed8e098941d11552a32957b968f57123404eae7262_1.jpg',
      'https://img.ibxk.com.br/ns/rexposta/2019/11/20/20212314402135.jpg?watermark=neaki&w=600',
      'https://cdn.discordapp.com/attachments/771814692460691480/777888712549072937/bf0cdb210bf86488f5e3d7aecbb36f26.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777888631200808980/3929c83560963e5852c6a96b9d64965a.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777888390170542090/43f3d1e66050c9c12bd5b068e12ef621.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777888241222811698/2d3cad0bb1ccf645f5a5c7c4c76b8472.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777888122452836402/b4238f91aea51b4ee11e1ef87b9b5346.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777887876947247140/b456ae9cf3d5871846e8d198049fa086.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/742506854349013142/unknown.png',
      'https://cdn.discordapp.com/attachments/712262248252571678/721056824186503168/FB_IMG_1585621022058-1.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/725976249167511562/104095659_3407093932655084_2001404512137427354_n.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/725989166814593024/106397691_900141417118668_2059026800708379367_n.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/725989281083949066/106205389_1605987732898605_6123879751023577540_n.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/725989472004735033/unknown.png',
      'https://cdn.discordapp.com/attachments/687398947588800518/724584749095452673/103413279_723124911771749_5948525329590399121_n.png',
      'https://cdn.discordapp.com/attachments/724845889373601892/726376689889706024/105594860_732517340832506_7299615619577528665_n.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777887711481954334/6f3244d39d93966be1e7b87e2294d352.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777887596369281054/9d8bf637ab3bbcb85de3f169f5bc0019.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777887336766898186/21cbf8f65c3c5e6c49d8aea61a284047.png',
      'https://cdn.discordapp.com/attachments/771814692460691480/777887111218200576/0b1004ae55d1573e3ee789f57a703525.png'
 ]

        imagem = random.choice(memes)
        avatar = ctx.author.display_avatar.url

        embed = discord.Embed(
            title="Memes",
            description=f"{ctx.author.mention} **Muitos Memes de anime**",
            color=discord.Color.random(),
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=imagem)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text="Memes")
        embed.set_author(name=ctx.author.display_name, icon_url=avatar)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))