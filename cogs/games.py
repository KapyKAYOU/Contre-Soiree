from discord.ext import commands
from utils.backup import backup_pseudos
from datetime import datetime
from utils.permission import (
    check_whitelist_channel,
    check_host_channel,
    can_manage,
    can_view,
    can_clear,
    check_thread_channel

)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() # Commande add 
    async def add(self, ctx, *, pseudos_texte: str):
        if not await check_whitelist_channel(ctx):
            return

        if not await can_manage(ctx):
            return

        pseudos_a_ajouter = pseudos_texte.split()

        try:
            with open("pseudos.txt", "r", encoding="utf-8") as f:
                pseudos_existants = f.read().splitlines()
        except FileNotFoundError:
            pseudos_existants = []

        ajoutes = []
        ignores = []

        for pseudo in pseudos_a_ajouter:
            if pseudo in pseudos_existants:
                ignores.append(pseudo)
            else:
                pseudos_existants.append(pseudo)
                ajoutes.append(pseudo)

        with open("pseudos.txt", "w", encoding="utf-8") as f:
            for p in pseudos_existants:
                f.write(p + "\n")

        message = ""

        if ajoutes:
            message += "✅ Ajoutés : " + ", ".join(ajoutes) + "\n"

        if ignores:
            message += "⚠️ Déjà présents : " + ", ".join(ignores)

        msg = await ctx.send(message)

        # Suppression rapide de la commande
        await ctx.message.delete(delay=1)

        # Suppression plus lente de la réponse
        await msg.delete(delay=2)

    @commands.command() # Commande Remove
    async def remove(self, ctx, *, pseudo: str):
        if not await check_whitelist_channel(ctx):
            return

        if not await can_manage(ctx):
            return
        try:
            with open("pseudos.txt", "r", encoding="utf-8") as f:
                pseudos = f.read().splitlines()
        except FileNotFoundError:
            pseudos = []

        if pseudo not in pseudos:
            msg = await ctx.send("❌ Ce pseudo n'est pas dans la liste.")
            try:
                await ctx.message.delete(delay=1)
            except:
                pass
            await msg.delete(delay=3)
            return

        pseudos.remove(pseudo)

        with open("pseudos.txt", "w", encoding="utf-8") as f:
            for p in pseudos:
                f.write(p + "\n")

        msg = await ctx.send(f"🗑 **{pseudo}** a été retiré de la liste.")

        # Suppression rapide de la commande
        try:
            await ctx.message.delete(delay=1)
        except:
            pass

        # Suppression plus lente de la réponse
        await msg.delete(delay=3)

    @commands.command() # Commande Edit 
    async def edit(self, ctx, old: str, new: str):
        if not await check_whitelist_channel(ctx):
            return

        if not await can_manage(ctx):
            return

        try:
            with open("pseudos.txt", "r", encoding="utf-8") as f:
                pseudos = f.read().splitlines()
        except FileNotFoundError:
            pseudos = []

        if old not in pseudos:
            msg = await ctx.send("❌ L'ancien pseudo n'est pas dans la liste.")
            await msg.delete(delay=3)
            return

        if new in pseudos:
            msg = await ctx.send("⚠️ Le nouveau pseudo est déjà présent.")
            await msg.delete(delay=3)
            return

        index = pseudos.index(old)
        pseudos[index] = new

        with open("pseudos.txt", "w", encoding="utf-8") as f:
            for p in pseudos:
                f.write(p + "\n")

        msg = await ctx.send(f"✏️ **{old}** a été remplacé par **{new}**.")

        try:
            await ctx.message.delete(delay=1)
        except:
            pass

        await msg.delete(delay=3)

    @commands.command() # Commande List
    async def list(self, ctx):
        if not await check_host_channel(ctx):
            return

        if not await can_view(ctx):
            return

        try:
            with open("pseudos.txt", "r", encoding="utf-8") as f:
                pseudos = f.read().splitlines()
        except FileNotFoundError:
            pseudos = []

        if not pseudos:
            msg = await ctx.send("📭 La liste est vide.")
            await ctx.message.delete(delay=1)
            await msg.delete(delay=5)
            return

        COL_SIZE = 15
        columns = [
            pseudos[i:i + COL_SIZE]
            for i in range(0, len(pseudos), COL_SIZE)
        ]

        lines = []
        max_rows = max(len(col) for col in columns)

        for row in range(max_rows):
            line = []
            for col_index, col in enumerate(columns):
                index = col_index * COL_SIZE + row
                if row < len(col):
                    line.append(f"{index+1:>2}. {col[row]:<16}")
                lines.append(" ".join(line))

        content = "```📋 Liste des pseudos\n\n" + "\n".join(lines) + "```"


        msg = await ctx.send(content)
        await ctx.message.delete(delay=1)
        await msg.delete(delay=30)

    @commands.command() # Commande Copy
    async def copy(self, ctx):
        if not await check_host_channel(ctx):
            return

        if not await can_view(ctx):
            return

        try:
            with open("pseudos.txt", "r", encoding="utf-8") as f:
                pseudos = f.read().splitlines()
        except FileNotFoundError:
            pseudos = []

        if not pseudos:
            msg = await ctx.send("📭 Aucun pseudo dans la whitelist.")
            await msg.delete(delay=5)
            await ctx.message.delete(delay=3)
            return

        PREFIX = "/wl add "
        MAX_LEN = 230

        messages = []
        current = PREFIX

        for pseudo in pseudos:
            if len(current) + len(pseudo) + 1 > MAX_LEN:
                messages.append(current.strip())
                current = PREFIX + pseudo + " "
            else:
                current += pseudo + " "

        if current.strip() != PREFIX.strip():
            messages.append(current.strip())

        for m in messages:
            await ctx.send(f"```{m}```")

        try:
            await ctx.message.delete(delay=2)
        except:
            pass

    @commands.command() # Commande Clear
    async def clear(self, ctx):
        if not await check_whitelist_channel(ctx):
            return

        if not await can_clear(ctx):
            return

        backup_file = backup_pseudos()  # 🔥 TA fonction existante

        with open("pseudos.txt", "w", encoding="utf-8"):
            pass

        msg_text = "🧹 Liste vidée."
        if backup_file:
            msg_text += f"\n📦 Backup créé : `{backup_file}`"

        msg = await ctx.send(msg_text)

        try:
            await ctx.message.delete(delay=3)
        except:
            pass

        await msg.delete(delay=6)

    @commands.command()
    async def startgame(self, ctx):

        # Salon obligatoire : annonce-host
        if not await check_thread_channel(ctx):
            return

        # Permission : HOST uniquement
        if not await can_view(ctx):
            return

        # Nom du thread
        date_str = datetime.now().strftime("%d-%m")
        host_name = ctx.author.display_name.replace(" ", "-").lower()
        thread_name = f"game-lg-{date_str}-{host_name}"

        # Message de base
        msg = await ctx.send(
            "🎮 **Thread de discussion de la game**\n"
            "Vous pouvez échanger ici pendant 24h 👇"
         )

        # Création du thread (24h)
        await msg.create_thread(
            name=thread_name,
            auto_archive_duration=1440
        )

        # Nettoyage
        try:
            await ctx.message.delete(delay=2)
        except:
         pass

async def setup(bot):
    await bot.add_cog(Games(bot))