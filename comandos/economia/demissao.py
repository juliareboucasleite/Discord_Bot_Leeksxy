import discord
from discord.ext import commands
import json
import os

class Demissao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances_file = "data/balances.json"
        self.empregos_file = "data/empregos.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.balances_file):
            with open(self.balances_file, "w") as f:
                json.dump({}, f)
        if not os.path.exists(self.empregos_file):
            with open(self.empregos_file, "w") as f:
                json.dump({}, f)
        with open(self.balances_file, "r") as f:
            self.balances = json.load(f)
        with open(self.empregos_file, "r") as f:
            self.empregos = json.load(f)

    def save_data(self):
        with open(self.balances_file, "w") as f:
            json.dump(self.balances, f, indent=2)
        with open(self.empregos_file, "w") as f:
            json.dump(self.empregos, f, indent=2)

    def get_money(self, uid):
        return self.balances.get(str(uid), {}).get("money", 0)

    def set_money(self, uid, amount):
        uid = str(uid)
        if uid not in self.balances:
            self.balances[uid] = {"money": 0, "bank": 0}
        self.balances[uid]["money"] = max(0, amount)

    def get_emprego(self, uid):
        return self.empregos.get(str(uid))

    def remove_emprego(self, uid):
        self.empregos.pop(str(uid), None)

    @commands.command(name="demissao", aliases=["demitir"])
    async def demitir(self, ctx):
        uid = str(ctx.author.id)
        saldo = self.get_money(uid)
        if saldo < 2000:
            return await ctx.send("💸 Para pedir demissão, você precisa de 2000 moedas.")
        emprego = self.get_emprego(uid)
        empregos_nomes = {
            1: "policial",
            2: "paramédico",
            3: "bombeiro"
        }
        if not emprego:
            return await ctx.send("💼 Você não possui um emprego para se demitir.")
        nome_emprego = empregos_nomes.get(emprego, "emprego desconhecido")
        msg = await ctx.send(
            f"📝 {ctx.author.mention}, você quer mesmo se demitir do emprego de **{nome_emprego}**?\n"
            f"💰 Será cobrada uma taxa de **2000 moedas**."
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except:
            return await ctx.send("⏰ Tempo esgotado. Demissão cancelada.")
        if str(reaction.emoji) == "✅":
            self.set_money(uid, saldo - 2000)
            self.remove_emprego(uid)
            self.save_data()
            await ctx.send("✅ Você foi demitido com sucesso.")
        else:
            await ctx.send("❌ Cancelado com sucesso.")

def setup(bot):
    bot.add_cog(Demissao(bot))
