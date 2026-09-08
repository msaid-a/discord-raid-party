import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

ROLES_CONFIG = {
    "Force User": 1,
    "Healer": 1,
    "Swordmaster": 1,
    "Tank": 1,
    "Ice Stack": 1,
    "Acrobat": 1,
    "DPS": 2,
}

TOTAL_SLOTS = 8

# View untuk Control Panel Host
class HostAssignView(discord.ui.View):
    def __init__(self, party_view):
        super().__init__(timeout=300)
        self.party_view = party_view
        self.selected_user = None

    @discord.ui.select(cls=discord.ui.UserSelect, placeholder="1. Pilih Player...", row=0)
    async def user_select(self, interaction: discord.Interaction, select: discord.ui.UserSelect):
        self.selected_user = select.values[0]
        await interaction.response.send_message(
            f"Player terpilih: {self.selected_user.mention}. Sekarang pilih role di bawah.", 
            ephemeral=True
        )

    @discord.ui.select(
        placeholder="2. Pilih Role / Tindakan...",
        options=[discord.SelectOption(label=r, value=r) for r in ROLES_CONFIG.keys()] + [discord.SelectOption(label="❌ Remove/Kick", value="Remove")],
        row=1
    )
    async def role_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if not self.selected_user:
            await interaction.response.send_message("⚠️ Silakan pilih player di dropdown paling atas terlebih dahulu!", ephemeral=True)
            return

        role_choice = select.values[0]
        user = self.selected_user

        # Hapus user dari semua role yang mungkin dia tempati sebelumnya
        for members in self.party_view.party_members.values():
            if user in members:
                members.remove(user)

        if role_choice != "Remove":
            # Cek limit slot
            if len(self.party_view.party_members[role_choice]) >= ROLES_CONFIG[role_choice]:
                await interaction.response.send_message(f"⚠️ Slot **{role_choice}** sudah penuh!", ephemeral=True)
                return
            
            # Masukkan ke role baru
            self.party_view.party_members[role_choice].append(user)
            await interaction.response.send_message(f"✅ Berhasil meng-assign {user.mention} ke **{role_choice}**.", ephemeral=True)
        else:
            await interaction.response.send_message(f"✅ Berhasil mengeluarkan {user.mention} dari party.", ephemeral=True)

        # Update tampilan utama Embed Party
        if self.party_view.message:
            await self.party_view.message.edit(embed=self.party_view.build_embed())


# View UI untuk Party Utama
class PartyView(discord.ui.View):
    def __init__(self, title: str, host: discord.User):
        super().__init__(timeout=None)
        self.title = title
        self.host = host
        self.is_open = True
        self.party_members = {role: [] for role in ROLES_CONFIG.keys()}
        self.message = None # Akan menyimpan referensi message ini agar bisa di-update dari Host Panel

    def get_total_joined(self):
        return sum(len(users) for users in self.party_members.values())

    def build_embed(self):
        embed = discord.Embed(
            title=self.title,
            color=discord.Color.from_rgb(47, 49, 54),
        )

        roles_text = ""
        for role_name, max_slot in ROLES_CONFIG.items():
            joined = self.party_members[role_name]
            slots_display = []

            for i in range(max_slot):
                if i < len(joined):
                    slots_display.append(joined[i].mention)
                else:
                    slots_display.append("*empty*")

            roles_text += f"**{role_name}** — {', '.join(slots_display)}\n"

        embed.add_field(name="Roles", value=roles_text, inline=False)

        total_joined = self.get_total_joined()
        status_str = (
            "🟢 Open" if self.is_open and total_joined < TOTAL_SLOTS else "🔴 Full/Closed"
        )

        embed.add_field(name="Host", value=self.host.mention, inline=True)
        embed.add_field(name="Slot", value=f"{total_joined}/{TOTAL_SLOTS}", inline=True)
        embed.add_field(name="Status", value=status_str, inline=True)

        embed.set_footer(text="Klik tombol role di bawah untuk join")
        return embed

    async def handle_join(self, interaction: discord.Interaction, role_name: str):
        user = interaction.user

        for r, members in self.party_members.items():
            if user in members:
                if r == role_name:
                    members.remove(user)
                    await interaction.response.edit_message(embed=self.build_embed())
                    return
                else:
                    await interaction.response.send_message(
                        f"Kamu sudah terdaftar sebagai **{r}**. Cancel/pindah role dulu!",
                        ephemeral=True,
                    )
                    return

        if len(self.party_members[role_name]) >= ROLES_CONFIG[role_name]:
            await interaction.response.send_message(
                f"Slot **{role_name}** sudah penuh!", ephemeral=True
            )
            return

        self.party_members[role_name].append(user)
        await interaction.response.edit_message(embed=self.build_embed())

    # --- Button Roles ---
    @discord.ui.button(label="Force User", style=discord.ButtonStyle.primary, emoji="🔴", row=0)
    async def btn_force_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Force User")

    @discord.ui.button(label="Healer", style=discord.ButtonStyle.primary, emoji="🏥", row=0)
    async def btn_healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Healer")

    @discord.ui.button(label="Swordmaster", style=discord.ButtonStyle.primary, emoji="🗡️", row=0)
    async def btn_swordmaster(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Swordmaster")

    @discord.ui.button(label="Tank", style=discord.ButtonStyle.primary, emoji="🛡️", row=1)
    async def btn_tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Tank")

    @discord.ui.button(label="Ice Stack", style=discord.ButtonStyle.primary, emoji="❄️", row=1)
    async def btn_ice_stack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Ice Stack")

    @discord.ui.button(label="Acrobat", style=discord.ButtonStyle.primary, emoji="🎯", row=1)
    async def btn_acrobat(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "Acrobat")

    @discord.ui.button(label="DPS", style=discord.ButtonStyle.primary, emoji="⚔️", row=1)
    async def btn_dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_join(interaction, "DPS")

    # --- Action Buttons ---
    @discord.ui.button(label="Cancel My Role", style=discord.ButtonStyle.secondary, row=2)
    async def btn_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        found = False
        for members in self.party_members.values():
            if user in members:
                members.remove(user)
                found = True
                break

        if found:
            await interaction.response.edit_message(embed=self.build_embed())
        else:
            await interaction.response.send_message("Kamu belum terdaftar di party ini.", ephemeral=True)

    @discord.ui.button(label="Create Party Thread", style=discord.ButtonStyle.blurple, emoji="💬", row=2)
    async def btn_create_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        target_forum_name = "💸gajian-salary"
        guild = interaction.guild

        forum_channel = discord.utils.get(guild.forums, name=target_forum_name)

        if not forum_channel:
            await interaction.response.send_message(
                f"Forum channel **#{target_forum_name}** tidak ditemukan! Pastikan nama channel sesuai dan berupa tipe Forum.",
                ephemeral=True,
            )
            return

        all_members = [
            user.mention for members in self.party_members.values() for user in members
        ]
        members_tag = ", ".join(all_members) if all_members else "Belum ada anggota"

        try:
            forum_post = await forum_channel.create_thread(
                name=self.title[:100],
                content=(
                    f"📌 **Thread Diskusi/Trade Party**: {self.title}\n"
                    f"**Host**: {self.host.mention}\n"
                    f"**Anggota**: {members_tag}"
                ),
                auto_archive_duration=1440,
            )
            
            await interaction.response.send_message(
                f"Thread berhasil dibuat di forum {forum_channel.mention} ➔ {forum_post.thread.mention}",
                ephemeral=True,
            )
        except Exception as e:
            await interaction.response.send_message(f"Gagal membuat thread di forum: {e}", ephemeral=True)

    # --- NEW: Host Control Button ---
    @discord.ui.button(label="Edit Roster (Host)", style=discord.ButtonStyle.danger, emoji="👑", row=2)
    async def btn_edit_roster(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Validasi hanya host yang boleh menekan
        if interaction.user.id != self.host.id:
            await interaction.response.send_message("🚫 Hanya host yang bisa mengakses menu pengaturan roster!", ephemeral=True)
            return

        # Simpan referensi ke message party saat ini agar bisa kita update nanti
        self.message = interaction.message 

        # Mengirimkan HostControlView yang baru (Dropdown assign player)
        await interaction.response.send_message(
            "👑 **Host Panel**\nPilih player lalu tentukan perannya, atau pilih Remove untuk mengeluarkan mereka.",
            view=HostAssignView(self),
            ephemeral=True
        )


@bot.event
async def on_ready():
    print(f"Bot recruitment ready: {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="createparty", description="Buat listing party raid baru")
@app_commands.describe(title="Judul Run/Raid (misal: DDNC 1X DICARRY TOHATO)")
async def create_party(interaction: discord.Interaction, title: str):
    view = PartyView(title=title, host=interaction.user)
    embed = view.build_embed()
    
    await interaction.response.send_message(content="@here", embed=embed, view=view)
    
    # Simpan objek pesannya ke dalam view agar bisa di-edit kapanpun
    view.message = await interaction.original_response()

bot.run(TOKEN)