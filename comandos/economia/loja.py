import discord
from discord.ext import commands
import json
import os
from typing import Optional

class Loja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = "economy.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.economy_data = json.load(f)
        else:
            self.economy_data = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.economy_data, f, indent=2)

    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.economy_data:
            self.economy_data[user_id] = {"money": 0, "bank": 0, "eventos": 0, "pet": None, "perfilfoto": None}
            self.save_data()
        return self.economy_data[user_id]

    @commands.command(name='loja', aliases=['shop'])
    async def loja(self, ctx, *, item: Optional[str] = None):
        user = self.get_user(ctx.author.id)
        money = user["money"]
        eventos = user.get("eventos", 0)

        pets = {
            "panda": 25000,
            "phoenix": 45000,
            "dragão": 85000,
            "flamingo": 5000,
            "blaze": 500000,
            "loli": 150000,
            "egirl": 250000
        }
        eventos_itens = {
            "surpresa1": 35,  # Boneco de neve
            "evento1": 45,    # Foto Happy Halloween
            "evento2": 45,    # Foto Happy Halloween gif
            "evento3": 45     # Foto Dragão
        }

        if not item:
            embed = discord.Embed(
                title="🛒 Loja de Pets e Eventos",
                description=(
                    "**Pets à venda:**\n" +
                    "\n".join([f"**{nome.title()}** | Preço: {preco:,} Réis" for nome, preco in pets.items()]) +
                    "\n\nDigite `!loja <nome do pet>` para comprar.\n\n" +
                    "**Loja de Evento:**\n" +
                    "Boneco de neve (`!loja surpresa1`) Preço: 35 CoinPet\n" +
                    "Foto no perfil Happy Halloween (`!loja evento1`) Preço: 45 CoinPet\n" +
                    "Foto no perfil Happy Halloween gif (`!loja evento2`) Preço: 45 CoinPet\n" +
                    "Foto no perfil Dragão (`!loja evento3`) Preço: 45 CoinPet"
                ),
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
            return

        item = item.lower()
        if item in pets:
            preco = pets[item]
            if money < preco:
                await ctx.send(f"❌ Você não tem {preco:,} Réis para a compra!")
                return
            user["pet"] = item
            user["money"] -= preco
            self.save_data()
            await ctx.send(f"✅ Você acaba de comprar um pet **{item.title()}** por {preco:,}R$!")
            return
        elif item in eventos_itens:
            preco = eventos_itens[item]
            if eventos < preco:
                await ctx.send(f"❌ Você não tem {preco} CoinPet para a compra!")
                return
            if item == "surpresa1":
                user["pet"] = "boneco de neve"
            else:
                user["perfilfoto"] = item
            user["eventos"] -= preco
            self.save_data()
            await ctx.send(f"✅ Você acaba de comprar o item de evento `{item}` por {preco} CoinPet!")
            return
        else:
            await ctx.send("❌ Item não encontrado na loja. Verifique o nome e tente novamente.")

async def setup(bot):
    await bot.add_cog(Loja(bot))
