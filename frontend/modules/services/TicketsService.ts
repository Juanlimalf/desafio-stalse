import type { TicketPriority, TicketStatus } from "@/modules/enum/TicketsEnum";
import type {
  GetTicketsFilters,
  Ticket,
  WebhookResponse,
} from "@/modules/interfaces/Tickets";

class TicketsService {
  private readonly baseUrl = `${process.env.BACKEND_URL ?? "http://127.0.0.1:8000"}/tickets/`;

  async getWebhook(): Promise<WebhookResponse> {
    const response = await fetch(`${this.baseUrl}webhook/`);

    if (!response.ok) throw new Error("Failed to fetch webhook");

    return response.json();
  }

  async modifyWebhook(url: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}webhook/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) throw new Error("Failed to modify webhook");
  }

  async getTickets(filters: GetTicketsFilters = {}): Promise<Ticket[]> {
    const params = new URLSearchParams();

    if (filters.customer_name)
      params.set("customer_name", filters.customer_name);
    if (filters.channel) params.set("channel", filters.channel);
    if (filters.status) params.set("status", filters.status);
    if (filters.priority) params.set("priority", filters.priority);

    const query = params.toString();
    const url = query ? `${this.baseUrl}?${query}` : this.baseUrl;

    const response = await fetch(url);

    if (!response.ok) throw new Error("Failed to fetch tickets");

    return response.json();
  }

  async getTicketById(ticketId: number): Promise<Ticket> {
    const response = await fetch(`${this.baseUrl}${ticketId}/`);

    if (!response.ok) throw new Error("Failed to fetch ticket by ID");

    return response.json();
  }

  async alterTicketStatusPriority(
    ticketId: number,
    status: TicketStatus,
    priority: TicketPriority,
  ): Promise<Ticket> {
    const response = await fetch(`${this.baseUrl}${ticketId}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status, priority }),
    });

    if (!response.ok)
      throw new Error("Failed to alter ticket status and priority");

    return response.json();
  }
}

export const ticketsService = new TicketsService();
