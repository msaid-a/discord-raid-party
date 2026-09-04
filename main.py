# # import discord
# # from discord import app_commands
# # from discord.ext import commands

# # TOKEN = "MTU0NTM5MzQ3MTQ1NDQ1MzgwMg.GT6oZw.oA2_pBLJjg8S4ba2ktvl7ajqarM-xtbN-t3NE4"

# # intents = discord.Intents.default()
# # bot = commands.Bot(command_prefix="!", intents=intents)

# # # Konfigurasi Role & Slot (Mercenary diganti menjadi DPS 2)
# # ROLES_CONFIG = {
# #     "Force User": 2,
# #     "Healer": 1,
# #     "DPS 2": 1,
# #     "Swordmaster": 1,
# #     "Tank": 1,
# #     "Ice Stack": 1,
# #     "Acrobat": 2,
# #     "DPS": 3,
# # }

# # TOTAL_SLOTS = 8


# # # View untuk Button Interaktif
# # class PartyView(discord.ui.View):

# #   def __init__(self, title: str, host: discord.User):
# #     super().__init__(timeout=None)
# #     self.title = title
# #     self.host = host
# #     self.is_open = True
# #     self.party_members = {role: [] for role in ROLES_CONFIG.keys()}

# #   def get_total_joined(self):
# #     return sum(len(users) for users in self.party_members.values())

# #   def build_embed(self):
# #     embed = discord.Embed(
# #         title=self.title,
# #         color=discord.Color.from_rgb(47, 49, 54),
# #     )

# #     roles_text = ""
# #     for role_name, max_slot in ROLES_CONFIG.items():
# #       joined = self.party_members[role_name]
# #       slots_display = []

# #       for i in range(max_slot):
# #         if i < len(joined):
# #           slots_display.append(joined[i].mention)
# #         else:
# #           slots_display.append("*empty*")

# #       roles_text += f"**{role_name}** — {', '.join(slots_display)}\n"

# #     embed.add_field(name="Roles", value=roles_text, inline=False)

# #     total_joined = self.get_total_joined()
# #     status_str = (
# #         "🟢 Open" if self.is_open and total_joined < TOTAL_SLOTS else "🔴 Full/Closed"
# #     )

# #     embed.add_field(name="Host", value=self.host.mention, inline=True)
# #     embed.add_field(
# #         name="Slot", value=f"{total_joined}/{TOTAL_SLOTS}", inline=True
# #     )
# #     embed.add_field(name="Status", value=status_str, inline=True)

# #     embed.set_footer(text="Klik tombol role di bawah untuk join")
# #     return embed

# #   async def handle_join(
# #       self, interaction: discord.Interaction, role_name: str
# #   ):
# #     user = interaction.user

# #     for r, members in self.party_members.items():
# #       if user in members:
# #         if r == role_name:
# #           members.remove(user)
# #           await interaction.response.edit_message(embed=self.build_embed())
# #           return
# #         else:
# #           await interaction.response.send_message(
# #               f"Kamu sudah terdaftar sebagai **{r}**. Cancel/pindah role dulu!",
# #               ephemeral=True,
# #           )
# #           return

# #     if len(self.party_members[role_name]) >= ROLES_CONFIG[role_name]:
# #       await interaction.response.send_message(
# #           f"Slot **{role_name}** sudah penuh!", ephemeral=True
# #       )
# #       return

# #     self.party_members[role_name].append(user)
# #     await interaction.response.edit_message(embed=self.build_embed())

# #   # --- Row 1 & 2: Button Role ---
# #   @discord.ui.button(
# #       label="Force User",
# #       style=discord.ButtonStyle.primary,
# #       emoji="🔴",
# #       row=0,
# #   )
# #   async def btn_force_user(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Force User")

# #   @discord.ui.button(
# #       label="Healer", style=discord.ButtonStyle.primary, emoji="🏥", row=0
# #   )
# #   async def btn_healer(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Healer")

# #   @discord.ui.button(
# #       label="DPS 2", style=discord.ButtonStyle.primary, emoji="⚔️", row=0
# #   )
# #   async def btn_dps_2(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "DPS 2")

# #   @discord.ui.button(
# #       label="Swordmaster",
# #       style=discord.ButtonStyle.primary,
# #       emoji="🗡️",
# #       row=0,
# #   )
# #   async def btn_swordmaster(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Swordmaster")

# #   @discord.ui.button(
# #       label="Tank", style=discord.ButtonStyle.primary, emoji="🛡️", row=1
# #   )
# #   async def btn_tank(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Tank")

# #   @discord.ui.button(
# #       label="Ice Stack", style=discord.ButtonStyle.primary, emoji="❄️", row=1
# #   )
# #   async def btn_ice_stack(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Ice Stack")

# #   @discord.ui.button(
# #       label="Acrobat", style=discord.ButtonStyle.primary, emoji="🎯", row=1
# #   )
# #   async def btn_acrobat(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "Acrobat")

# #   @discord.ui.button(
# #       label="DPS", style=discord.ButtonStyle.primary, emoji="⚔️", row=1
# #   )
# #   async def btn_dps(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     await self.handle_join(interaction, "DPS")

# #   # --- Row 3: Action Buttons ---
# #   @discord.ui.button(
# #       label="Cancel My Role",
# #       style=discord.ButtonStyle.secondary,
# #       row=2,
# #   )
# #   async def btn_cancel(
# #       self, interaction: discord.Interaction, button: discord.ui.Button
# #   ):
# #     user = interaction.user
# #     found = False
# #     for members in self.party_members.values():
# #       if user in members:
# #         members.remove(user)
# #         found = True
# #         break

# #     if found:
# #       await interaction.response.edit_message(embed=self.build_embed())
# #     else:
# #       await interaction.response.send_message(
# #           "Kamu belum terdaftar di party ini.", ephemeral=True
# #       )


# # @bot.event
# # async def on_ready():
# #   print(f"Bot recruitment ready: {bot.user}")
# #   await bot.tree.sync()


# # @bot.tree.command(
# #     name="createparty", description="Buat listing party raid baru"
# # )
# # @app_commands.describe(title="Judul Run/Raid (misal: DDNC 1X DICARRY TOHATO)")
# # async def create_party(interaction: discord.Interaction, title: str):
# #   view = PartyView(title=title, host=interaction.user)
# #   embed = view.build_embed()
# #   await interaction.response.send_message(
# #       content="@here", embed=embed, view=view
# #   )


# # bot.run(TOKEN)

# import discord
# from discord import app_commands
# from discord.ext import commands

# TOKEN = "MTU0NTM5MzQ3MTQ1NDQ1MzgwMg.GT6oZw.oA2_pBLJjg8S4ba2ktvl7ajqarM-xtbN-t3NE4"

# intents = discord.Intents.default()
# bot = commands.Bot(command_prefix="!", intents=intents)

# ROLES_CONFIG = {
#     "Force User": 1,
#     "Healer": 1,
#     "DPS 2": 1,
#     "Swordmaster": 1,
#     "Tank": 1,
#     "Ice Stack": 1,
#     "Acrobat": 1,
#     "DPS": 1,
# }

# TOTAL_SLOTS = 8

# # View UI untuk Button Interaktif
# class PartyView(discord.ui.View):

#   def __init__(self, title: str, host: discord.User):
#     super().__init__(timeout=None)
#     self.title = title
#     self.host = host
#     self.is_open = True
#     self.party_members = {role: [] for role in ROLES_CONFIG.keys()}

#   def get_total_joined(self):
#     return sum(len(users) for users in self.party_members.values())

#   def build_embed(self):
#     embed = discord.Embed(
#         title=self.title,
#         color=discord.Color.from_rgb(47, 49, 54),
#     )

#     roles_text = ""
#     for role_name, max_slot in ROLES_CONFIG.items():
#       joined = self.party_members[role_name]
#       slots_display = []

#       for i in range(max_slot):
#         if i < len(joined):
#           slots_display.append(joined[i].mention)
#         else:
#           slots_display.append("*empty*")

#       roles_text += f"**{role_name}** — {', '.join(slots_display)}\n"

#     embed.add_field(name="Roles", value=roles_text, inline=False)

#     total_joined = self.get_total_joined()
#     status_str = (
#         "🟢 Open" if self.is_open and total_joined < TOTAL_SLOTS else "🔴 Full/Closed"
#     )

#     embed.add_field(name="Host", value=self.host.mention, inline=True)
#     embed.add_field(
#         name="Slot", value=f"{total_joined}/{TOTAL_SLOTS}", inline=True
#     )
#     embed.add_field(name="Status", value=status_str, inline=True)

#     embed.set_footer(text="Klik tombol role di bawah untuk join")
#     return embed

#   async def handle_join(
#       self, interaction: discord.Interaction, role_name: str
#   ):
#     user = interaction.user

#     for r, members in self.party_members.items():
#       if user in members:
#         if r == role_name:
#           members.remove(user)
#           await interaction.response.edit_message(embed=self.build_embed())
#           return
#         else:
#           await interaction.response.send_message(
#               f"Kamu sudah terdaftar sebagai **{r}**. Cancel/pindah role dulu!",
#               ephemeral=True,
#           )
#           return

#     if len(self.party_members[role_name]) >= ROLES_CONFIG[role_name]:
#       await interaction.response.send_message(
#           f"Slot **{role_name}** sudah penuh!", ephemeral=True
#       )
#       return

#     self.party_members[role_name].append(user)
#     await interaction.response.edit_message(embed=self.build_embed())

#   # --- Button Roles ---
#   @discord.ui.button(
#       label="Force User",
#       style=discord.ButtonStyle.primary,
#       emoji="🔴",
#       row=0,
#   )
#   async def btn_force_user(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Force User")

#   @discord.ui.button(
#       label="Healer", style=discord.ButtonStyle.primary, emoji="🏥", row=0
#   )
#   async def btn_healer(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Healer")

#   @discord.ui.button(
#       label="DPS 2", style=discord.ButtonStyle.primary, emoji="⚔️", row=0
#   )
#   async def btn_dps_2(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "DPS 2")

#   @discord.ui.button(
#       label="Swordmaster",
#       style=discord.ButtonStyle.primary,
#       emoji="🗡️",
#       row=0,
#   )
#   async def btn_swordmaster(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Swordmaster")

#   @discord.ui.button(
#       label="Tank", style=discord.ButtonStyle.primary, emoji="🛡️", row=1
#   )
#   async def btn_tank(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Tank")

#   @discord.ui.button(
#       label="Ice Stack", style=discord.ButtonStyle.primary, emoji="❄️", row=1
#   )
#   async def btn_ice_stack(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Ice Stack")

#   @discord.ui.button(
#       label="Acrobat", style=discord.ButtonStyle.primary, emoji="🎯", row=1
#   )
#   async def btn_acrobat(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "Acrobat")

#   @discord.ui.button(
#       label="DPS", style=discord.ButtonStyle.primary, emoji="⚔️", row=1
#   )
#   async def btn_dps(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     await self.handle_join(interaction, "DPS")

#   # --- Action Buttons ---
#   @discord.ui.button(
#       label="Cancel My Role", style=discord.ButtonStyle.secondary, row=2
#   )
#   async def btn_cancel(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     user = interaction.user
#     found = False
#     for members in self.party_members.values():
#       if user in members:
#         members.remove(user)
#         found = True
#         break

#     if found:
#       await interaction.response.edit_message(embed=self.build_embed())
#     else:
#       await interaction.response.send_message(
#           "Kamu belum terdaftar di party ini.", ephemeral=True
#       )

#   # --- Tombol Create Thread Khusus ke Forum Channel ---
#   @discord.ui.button(
#       label="Create Party Thread",
#       style=discord.ButtonStyle.blurple,
#       emoji="💬",
#       row=2,
#   )
#   async def btn_create_thread(
#       self, interaction: discord.Interaction, button: discord.ui.Button
#   ):
#     target_forum_name = "💸gajian-salary"
#     guild = interaction.guild

#     # Cari Forum Channel bernama 💸gajian-salary
#     forum_channel = discord.utils.get(
#         guild.forums, name=target_forum_name
#     )

#     if not forum_channel:
#       await interaction.response.send_message(
#           f"Forum channel **#{target_forum_name}** tidak ditemukan! Pastikan nama channel sesuai dan berupa tipe Forum.",
#           ephemeral=True,
#       )
#       return

#     # Ambil daftar member yang sudah join
#     all_members = [
#         user.mention
#         for members in self.party_members.values()
#         for user in members
#     ]
#     members_tag = (
#         ", ".join(all_members) if all_members else "Belum ada anggota"
#     )

#     # Buat Post/Thread baru di dalam Forum Channel tersebut
#     try:
#       forum_post = await forum_channel.create_thread(
#           name=self.title[:100],  # Judul Post Forum dibatasi 100 karakter
#           content=(
#               f"📌 **Thread Diskusi/Trade Party**: {self.title}\n"
#               f"**Host**: {self.host.mention}\n"
#               f"**Anggota**: {members_tag}"
#           ),
#           auto_archive_duration=1440,
#       )
      
#       await interaction.response.send_message(
#           f"Thread berhasil dibuat di forum {forum_channel.mention} ➔ {forum_post.thread.mention}",
#           ephemeral=True,
#       )
#     except Exception as e:
#       await interaction.response.send_message(
#           f"Gagal membuat thread di forum: {e}", ephemeral=True
#       )


# @bot.event
# async def on_ready():
#   print(f"Bot recruitment ready: {bot.user}")
#   await bot.tree.sync()


# # Slash Command /createparty dikembalikan agar bisa dipanggil di channel teks mana saja
# # ... (kode bot, class PartyView, dan events di atasnya biarkan sama) ...

# @bot.tree.command(
#     name="createparty", description="Buat listing party raid baru"
# )
# @app_commands.describe(title="Judul Run/Raid (misal: DDNC 1X DICARRY TOHATO)")
# async def create_party(interaction: discord.Interaction, title: str):
#   view = PartyView(title=title, host=interaction.user)
#   embed = view.build_embed()
  
#   await interaction.response.send_message(
#       content="@here", embed=embed, view=view
#   )

# # --- KONFIGURASI KHUSUS VERCEL & FLASK ---
# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Bot Discord Party Recruitment berjalan di Vercel!"

# # Vercel akan mencari variabel 'app' ini untuk dijalankan sebagai WSGI app
# if __name__ == "__main__":
#     app.run(debug=True)

import os
from flask import Flask, jsonify, request
from nacl.exceptions import BadSignatureError
from nacl.public import VerifyKey

app = Flask(__name__)

# Ambil Public Key dari Discord Developer Portal (bukan Bot Token!)
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")


def verify_discord_signature(request_data, signature, timestamp, public_key):
  try:
    verify_key = VerifyKey(bytes.fromhex(public_key))
    verify_key.verify(
        f"{timestamp}{request_data}".encode(), bytes.fromhex(signature)
    )
    return True
  except (BadSignatureError, ValueError):
    return False


@app.route("/", methods=["POST"])
def interactions():
  # Verifikasi keamanan dari Discord
  signature = request.headers.get("X-Signature-Ed25519")
  timestamp = request.headers.get("X-Signature-Timestamp")
  body = request.get_data().decode("utf-8")

  if not signature or not timestamp or not verify_discord_signature(body, signature, timestamp, '93b3849685e6e2cf52fbb4d355a78390c1f293406bd2c2abc57ad9fd67ce2204'):
    return "Invalid request signature", 401

  data = request.json
  interaction_type = data.get("type")

  # 1. PING (Discord melakukan verifikasi URL Endpoint)
  if interaction_type == 1:
    return jsonify({"type": 1})

  # 2. APPLICATION_COMMAND (Slash Command dipanggil)
  if interaction_type == 2:
    command_name = data.get("data", {}).get("name")

    if command_name == "createparty":
      return jsonify({
          "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE (Balas pesan)
          "data": {
              "content": "Party berhasil dibuat via Vercel Webhook!"
          },
      })

  return jsonify({"error": "Unknown interaction"}), 400


@app.route("/", methods=["GET"])
def home():
  return "Discord Interaction Webhook aktif di Vercel!"


if __name__ == "__main__":
  app.run(debug=True)