import { ticketsService } from "@/modules/services/TicketsService";
import { BackButton } from "./components/BackButton";
import { TicketsTable } from "./components/TicketsTable";
import { WebhookCard } from "./components/WebhookCard";

export default async function TicketsPage() {
  const [tickets, webhook] = await Promise.all([
    ticketsService.getTickets(),
    ticketsService.getWebhook(),
  ]);

  return (
    <main className="flex min-h-screen flex-col items-center px-4 py-12">
      <div className="w-full max-w-6xl">
        <BackButton />
      </div>
      <div className="w-full max-w-6xl">
        <h1 className="mb-6 text-2xl font-bold text-gray-900">Tickets</h1>

        <WebhookCard url={webhook.url} />

        <TicketsTable tickets={tickets} />
      </div>
    </main>
  );
}
