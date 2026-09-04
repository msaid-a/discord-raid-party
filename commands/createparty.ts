import {
  EmbedBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  ChannelType,
  type ButtonInteraction,
  type User,
} from "discord.js";
import type {
  CommandData,
  CommandExecuteResult,
  SimplifiedInteraction,
} from "../utils/types";

const ROLES_CONFIG: Record<string, number> = {
  "Force User": 1,
  Healer: 1,
  "DPS 2": 1,
  Swordmaster: 1,
  Tank: 1,
  "Ice Stack": 1,
  Acrobat: 1,
  DPS: 1,
};

const ROLE_EMOJI: Record<string, string> = {
  "Force User": "🔴",
  Healer: "🏥",
  "DPS 2": "⚔️",
  Swordmaster: "🗡️",
  Tank: "🛡️",
  "Ice Stack": "❄️",
  Acrobat: "🎯",
  DPS: "⚔️",
};

const TOTAL_SLOTS = 8;
const FORUM_CHANNEL_NAME = "💸gajian-salary";

class PartyState {
  title: string;
  host: User;
  isOpen = true;
  partyMembers: Record<string, User[]>;

  constructor(title: string, host: User) {
    this.title = title;
    this.host = host;
    this.partyMembers = Object.fromEntries(
      Object.keys(ROLES_CONFIG).map((role) => [role, [] as User[]])
    );
  }

  getTotalJoined(): number {
    return Object.values(this.partyMembers).reduce(
      (sum, users) => sum + users.length,
      0
    );
  }

  buildEmbed(): EmbedBuilder {
    let rolesText = "";
    for (const [roleName, maxSlot] of Object.entries(ROLES_CONFIG)) {
      const joined = this.partyMembers[roleName];
      const slots: string[] = [];
      for (let i = 0; i < maxSlot; i++) {
        slots.push(i < joined.length ? `<@${joined[i].id}>` : "*empty*");
      }
      rolesText += `**${roleName}** — ${slots.join(", ")}\n`;
    }

    const totalJoined = this.getTotalJoined();
    const statusStr =
      this.isOpen && totalJoined < TOTAL_SLOTS ? "🟢 Open" : "🔴 Full/Closed";

    return new EmbedBuilder()
      .setTitle(this.title)
      .setColor([47, 49, 54])
      .addFields(
        { name: "Roles", value: rolesText, inline: false },
        { name: "Host", value: `<@${this.host.id}>`, inline: true },
        { name: "Slot", value: `${totalJoined}/${TOTAL_SLOTS}`, inline: true },
        { name: "Status", value: statusStr, inline: true }
      )
      .setFooter({ text: "Klik tombol role di bawah untuk join" });
  }

  buildComponents(): ActionRowBuilder<ButtonBuilder>[] {
    const roleNames = Object.keys(ROLES_CONFIG);
    const row0 = roleNames.slice(0, 4);
    const row1 = roleNames.slice(4, 8);

    const toButton = (roleName: string) =>
      new ButtonBuilder()
        .setCustomId(`join:${roleName}`)
        .setLabel(roleName)
        .setEmoji(ROLE_EMOJI[roleName])
        .setStyle(ButtonStyle.Primary);

    const row2 = new ActionRowBuilder<ButtonBuilder>().addComponents(
      new ButtonBuilder()
        .setCustomId("cancel")
        .setLabel("Cancel My Role")
        .setStyle(ButtonStyle.Secondary),
      new ButtonBuilder()
        .setCustomId("createThread")
        .setLabel("Create Party Thread")
        .setEmoji("💬")
        .setStyle(ButtonStyle.Primary)
    );

    return [
      new ActionRowBuilder<ButtonBuilder>().addComponents(row0.map(toButton)),
      new ActionRowBuilder<ButtonBuilder>().addComponents(row1.map(toButton)),
      row2,
    ];
  }

  handleJoin(user: User, roleName: string): string | null {
    for (const [r, members] of Object.entries(this.partyMembers)) {
      const idx = members.findIndex((u) => u.id === user.id);
      if (idx !== -1) {
        if (r === roleName) {
          members.splice(idx, 1);
          return null;
        }
        return `Kamu sudah terdaftar sebagai **${r}**. Cancel/pindah role dulu!`;
      }
    }

    if (this.partyMembers[roleName].length >= ROLES_CONFIG[roleName]) {
      return `Slot **${roleName}** sudah penuh!`;
    }

    this.partyMembers[roleName].push(user);
    return null;
  }

  handleCancel(user: User): boolean {
    for (const members of Object.values(this.partyMembers)) {
      const idx = members.findIndex((u) => u.id === user.id);
      if (idx !== -1) {
        members.splice(idx, 1);
        return true;
      }
    }
    return false;
  }
}

// In-memory store for party state mapping message IDs to PartyState
const parties = new Map<string, PartyState>();

export default {
  data: {
    name: "createparty",
    description: "Buat listing party raid baru",
    options: [
      {
        name: "title",
        description: "Judul Run/Raid (misal: DDNC 1X DICARRY TOHATO)",
        type: 3, // String type in Discord API
        required: true,
      },
    ],
  } as unknown as CommandData,

  async execute(data: {
    interaction: SimplifiedInteraction;
  }): CommandExecuteResult {
    const { interaction } = data;
    const title = interaction.options.getString("title", true);
    const state = new PartyState(title, interaction.user);

    // Send the party panel
    const reply = await interaction.reply({
      content: "@here",
      embeds: [state.buildEmbed()],
      components: state.buildComponents(),
      fetchReply: true,
    });

    parties.set(reply.id, state);
    return;
  },
};

// Export handler helper if Discraft handles component/button routing globally,
// or place button interactions inside your Discraft interaction handler router.
export async function handlePartyButton(interaction: ButtonInteraction) {
  const state = parties.get(interaction.message.id);
  if (!state) {
    await interaction.reply({
      content: "Party ini sudah tidak aktif (bot mungkin baru saja restart).",
      ephemeral: true,
    });
    return;
  }

  const customId = interaction.customId;

  if (customId.startsWith("join:")) {
    const roleName = customId.slice("join:".length);
    const error = state.handleJoin(interaction.user, roleName);
    if (error) {
      await interaction.reply({ content: error, ephemeral: true });
      return;
    }
    await interaction.update({ embeds: [state.buildEmbed()] });
    return;
  }

  if (customId === "cancel") {
    const found = state.handleCancel(interaction.user);
    if (found) {
      await interaction.update({ embeds: [state.buildEmbed()] });
    } else {
      await interaction.reply({
        content: "Kamu belum terdaftar di party ini.",
        ephemeral: true,
      });
    }
    return;
  }

  if (customId === "createThread") {
    const guild = interaction.guild;
    if (!guild) {
      await interaction.reply({
        content: "Command ini hanya bisa dipakai di dalam server.",
        ephemeral: true,
      });
      return;
    }

    const forumChannel = guild.channels.cache.find(
      (c) => c.type === ChannelType.GuildForum && c.name === FORUM_CHANNEL_NAME
    );

    if (!forumChannel || forumChannel.type !== ChannelType.GuildForum) {
      await interaction.reply({
        content: `Forum channel **#${FORUM_CHANNEL_NAME}** tidak ditemukan! Pastikan nama channel sesuai dan berupa tipe Forum.`,
        ephemeral: true,
      });
      return;
    }

    const allMembers = Object.values(state.partyMembers)
      .flat()
      .map((user) => `<@${user.id}>`);
    const membersTag = allMembers.length ? allMembers.join(", ") : "Belum ada anggota";

    try {
      const forumPost = await forumChannel.threads.create({
        name: state.title.slice(0, 100),
        message: {
          content:
            `📌 **Thread Diskusi/Trade Party**: ${state.title}\n` +
            `**Host**: <@${state.host.id}>\n` +
            `**Anggota**: ${membersTag}`,
        },
        autoArchiveDuration: 1440,
      });

      await interaction.reply({
        content: `Thread berhasil dibuat di forum <#${forumChannel.id}> ➔ <#${forumPost.id}>`,
        ephemeral: true,
      });
    } catch (e) {
      await interaction.reply({
        content: `Gagal membuat thread di forum: ${e}`,
        ephemeral: true,
      });
    }
  }
}