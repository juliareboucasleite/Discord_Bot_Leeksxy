import discord
from discord.ext import commands
import json
import os

# Função XP simulada
def get_info(xp):
    level = 0
    levelxp = 100
    total = xp
    while total >= levelxp:
        total -= levelxp
        level += 1
        levelxp += 20
    return {
        "level": level,
        "remxp": total,
        "levelxp": levelxp
    }

class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pets_file = "data/pets.json"
        self.xp_file = "data/pets_xp.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.pets_file):
            with open(self.pets_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.xp_file):
            with open(self.xp_file, "w") as f:
                json.dump({}, f)
        with open(self.pets_file, "r") as f:
            self.pets = json.load(f)
        with open(self.xp_file, "r") as f:
            self.xp = json.load(f)

    def save_data(self):
        with open(self.pets_file, "w") as f:
            json.dump(self.pets, f, indent=4)
        with open(self.xp_file, "w") as f:
            json.dump(self.xp, f, indent=4)

    @commands.command(name="pet", aliases=["animal"])
    async def pet(self, ctx):
        user = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
        user_id = str(user.id)
        guild_id = str(ctx.guild.id)
        emoji = "🐾"
        pet_id = self.pets.get(user_id, {}).get("pet", None)
        pets = {
            None: "https://conteudo.imguol.com.br/c/entretenimento/54/2020/04/28/cachorro-pug-1588098472110_v2_1920x1281.jpg",
            909090: "https://i.imgur.com/N8HBlPT.png",
            303030: "https://imgur.com/cKTZ6V5.png",
            403929: "https://alquimiadaalma.com.br/wp-content/uploads/2018/01/Drag%C3%A3o-Dourado1-2-1030x561.jpg",
            759203: "https://i.pinimg.com/originals/09/9d/30/099d30c1cd93130d17bc0d34247f80d0.jpg",
            182306: "https://gamepedia.cursecdn.com/minecraft_gamepedia/5/5a/Blaze.gif",
            999999: "https://i.pinimg.com/originals/22/c7/95/22c795a87fb8f21051f087ee1940c334.jpg",
            100000: "https://i.ibb.co/C7Xt284/Sem-T-tulo-1.jpg",
            100001: "https://i.pinimg.com/originals/90/fe/f1/90fef1264e0a211c8ae9c8305ff48c50.jpg",
            100002: "https://cdn.discordapp.com/attachments/749707196350070804/761218685863067728/picky-jones-lil-peep.jpg",
            100003: "https://pa1.narvii.com/6358/5296bf3d6e7d859c8081f3c0dc0344598ba761ab_hq.gif",
            100004: "https://danbooru.donmai.us/data/__seraphine_league_of_legends__2a3ad80223ec596098738ccd59b48994.jpg",
            12: "https://pm1.narvii.com/6476/939dc20919ee3fd92499e7c2dfa972dc3f79d4cd_00.jpg",
            99: "https://thumbs.gfycat.com/DrearyTeemingAtlanticblackgoby-small.gif"
        }
        pet_image = pets.get(pet_id, pets[None])
        xp_key = f"{user_id}_{guild_id}"
        xp = self.xp.get(xp_key, 0)
        info = get_info(xp)
        embed = discord.Embed(
            color=discord.Color.red(),
            title=f"Animal de estimação do {user.display_name}",
        )
        embed.set_author(name="🐾 Animal de estimação 🐾")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_image(url=pet_image)
        embed.add_field(
            name="**Level Do Pet**",
            value=f"{emoji} Level {info['level']} \n<:emoji_13:744871330880421958> XP {info['remxp']}/{info['levelxp']}",
            inline=False
        )
        embed.add_field(
            name="**Segue lá**",
            value="[**Twitter do Parceiro**](https://twitter.com/AncherArttz)",
            inline=False
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pet(bot))
