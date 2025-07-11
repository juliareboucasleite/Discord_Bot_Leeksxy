import discord
from discord.ext import commands
import random
from utils.ship_image import create_ship_image

class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ship')
    async def ship(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        if not member2:
            await ctx.send("💞 Mencione duas pessoas para fazer o ship.")
            return

        member1 = member1 or ctx.author

        seed = hash(str(sorted([member1.id, member2.id])))
        random.seed(seed)
        percentage = random.randint(0, 100)

        image = create_ship_image(
            member1.display_avatar.url,
            member2.display_avatar.url,
            percentage
        )

        file = discord.File(image, filename="ship.png")
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(Ship(bot))
