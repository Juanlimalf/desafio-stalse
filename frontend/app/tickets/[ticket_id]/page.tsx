import {
  CHANNEL_COLORS,
  CHANNEL_LABELS,
  PRIORITY_LABELS,
  STATUS_LABELS,
} from "@/modules/mappers/TicketsMappers";
import { ticketsService } from "@/modules/services/TicketsService";
import { Badge } from "flowbite-react";
import { BackButton } from "../components/BackButton";
import { TicketUpdateModal } from "../components/TicketUpdateModal";

type Props = {
  params: Promise<{ ticket_id: string }>;
};

export default async function TicketsDetailPage({ params }: Readonly<Props>) {
  const { ticket_id } = await params;
  const ticket = await ticketsService.getTicketById(Number(ticket_id));

  return (
    <main className="flex min-h-screen flex-col items-center px-4 py-12">
      <div className="w-full max-w-6xl">
        <BackButton />

        <h1 className="mb-6 text-2xl font-bold text-gray-900">
          Ticket {ticket.id} - {ticket.subject}
        </h1>

        <div className="grid grid-cols-3 gap-4 border border-gray-200 bg-gray-50 p-4">
          <div>
            <p className="text-sm text-gray-500">Cliente</p>
            <p className="text-gray-900">{ticket.customer_name}</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Canal</p>
            <Badge color={CHANNEL_COLORS[ticket.channel]} className="w-fit">
              {CHANNEL_LABELS[ticket.channel]}
            </Badge>
          </div>

          <div>
            <p className="text-sm text-gray-500">Status</p>
            <Badge color="success" className="w-fit">
              {STATUS_LABELS[ticket.status]}
            </Badge>
          </div>

          <div>
            <p className="text-sm text-gray-500">Prioridade</p>
            <Badge color="warning" className="w-fit">
              {PRIORITY_LABELS[ticket.priority]}
            </Badge>
          </div>

          <div>
            <p className="text-sm text-gray-500">Data de criação</p>
            <p className="text-gray-900">
              {new Date(ticket.created_at).toLocaleString("pt-BR")}
            </p>
          </div>
        </div>

        <div className="mt-4">
          <TicketUpdateModal ticket={ticket} />
        </div>
      </div>
    </main>
  );
}
