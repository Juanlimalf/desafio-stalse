import type {
  TicketChannel,
  TicketPriority,
  TicketStatus,
} from "@/modules/enum/TicketsEnum";

type WebhookResponse = {
  url: string;
};

type Ticket = {
  id: number;
  created_at: string;
  customer_name: string;
  channel: TicketChannel;
  subject: string;
  status: TicketStatus;
  priority: TicketPriority;
};

type GetTicketsFilters = {
  customer_name?: string;
  channel?: TicketChannel;
  status?: TicketStatus;
  priority?: TicketPriority;
};
