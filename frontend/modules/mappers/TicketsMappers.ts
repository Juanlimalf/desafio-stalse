import {
  TicketChannel,
  TicketPriority,
  TicketStatus,
} from "@/modules/enum/TicketsEnum";

export const CHANNEL_LABELS: Record<TicketChannel, string> = {
  [TicketChannel.Whatsapp]: "WhatsApp",
  [TicketChannel.Email]: "E-mail",
  [TicketChannel.Chat]: "Chat",
  [TicketChannel.Telefone]: "Telefone",
  [TicketChannel.Instagram]: "Instagram",
};

export const CHANNEL_COLORS: Record<TicketChannel, string> = {
  [TicketChannel.Whatsapp]: "success",
  [TicketChannel.Email]: "gray",
  [TicketChannel.Chat]: "info",
  [TicketChannel.Telefone]: "warning",
  [TicketChannel.Instagram]: "failure",
};

export const STATUS_LABELS: Record<TicketStatus, string> = {
  [TicketStatus.Opened]: "Aberto",
  [TicketStatus.Closed]: "Fechado",
};

export const STATUS_COLORS: Record<TicketStatus, string> = {
  [TicketStatus.Opened]: "success",
  [TicketStatus.Closed]: "gray",
};

export const PRIORITY_LABELS: Record<TicketPriority, string> = {
  [TicketPriority.Low]: "Baixa",
  [TicketPriority.Medium]: "Média",
  [TicketPriority.High]: "Alta",
};

export const PRIORITY_COLORS: Record<TicketPriority, string> = {
  [TicketPriority.Low]: "gray",
  [TicketPriority.Medium]: "warning",
  [TicketPriority.High]: "failure",
};
