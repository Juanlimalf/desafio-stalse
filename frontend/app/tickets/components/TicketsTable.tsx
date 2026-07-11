"use client";

import {
  TicketChannel,
  TicketPriority,
  TicketStatus,
} from "@/modules/enum/TicketsEnum";
import type { Ticket } from "@/modules/interfaces/Tickets";
import {
  CHANNEL_COLORS,
  CHANNEL_LABELS,
  PRIORITY_COLORS,
  PRIORITY_LABELS,
  STATUS_COLORS,
  STATUS_LABELS,
} from "@/modules/mappers/TicketsMappers";
import { ticketsService } from "@/modules/services/TicketsService";
import {
  Badge,
  Select,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
  TextInput,
} from "flowbite-react";
import { useEffect, useState } from "react";

type Props = {
  tickets: Ticket[];
};

export function TicketsTable({ tickets }: Readonly<Props>) {
  const [filteredTickets, setFilteredTickets] = useState(tickets);
  const [customerName, setCustomerName] = useState("");
  const [channel, setChannel] = useState("");
  const [status, setStatus] = useState("");
  const [priority, setPriority] = useState("");

  useEffect(() => {
    let active = true;

    ticketsService
      .getTickets({
        customer_name: customerName.trim() || undefined,
        channel: (channel || undefined) as TicketChannel | undefined,
        status: (status || undefined) as TicketStatus | undefined,
        priority: (priority || undefined) as TicketPriority | undefined,
      })
      .then((data) => {
        if (active) setFilteredTickets(data);
      });

    return () => {
      active = false;
    };
  }, [customerName, channel, status, priority]);

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-flow-row-dense grid-cols-5 gap-3">
        <div className="col-span-2">
          <TextInput
            placeholder="Buscar por cliente"
            value={customerName}
            onChange={(event) => setCustomerName(event.target.value)}
          />
        </div>
        <div>
          <Select
            value={channel}
            onChange={(event) => setChannel(event.target.value)}
          >
            <option value={""}>Todos os canais</option>
            {Object.values(TicketChannel).map((value) => (
              <option key={value} value={value}>
                {CHANNEL_LABELS[value]}
              </option>
            ))}
          </Select>
        </div>
        <div>
          <Select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
          >
            <option value={""}>Todos os status</option>
            {Object.values(TicketStatus).map((value) => (
              <option key={value} value={value}>
                {STATUS_LABELS[value]}
              </option>
            ))}
          </Select>
        </div>
        <div>
          <Select
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
          >
            <option value={""}>Todas as prioridades</option>
            {Object.values(TicketPriority).map((value) => (
              <option key={value} value={value}>
                {PRIORITY_LABELS[value]}
              </option>
            ))}
          </Select>
        </div>
      </div>

      <p className="text-sm text-gray-500">
        {filteredTickets.length} de {tickets.length} tickets
      </p>

      <div className="overflow-x-auto">
        <Table>
          <TableHead>
            <TableRow>
              <TableHeadCell>Data</TableHeadCell>
              <TableHeadCell>Cliente</TableHeadCell>
              <TableHeadCell>Canal</TableHeadCell>
              <TableHeadCell>Assunto</TableHeadCell>
              <TableHeadCell>Status</TableHeadCell>
              <TableHeadCell>Prioridade</TableHeadCell>
              <TableHeadCell>Ações</TableHeadCell>
            </TableRow>
          </TableHead>
          <TableBody className="divide-y">
            {filteredTickets.map((ticket) => (
              <TableRow key={ticket.id} className="bg-white">
                <TableCell className="whitespace-nowrap">
                  {new Date(ticket.created_at).toLocaleString("pt-BR")}
                </TableCell>
                <TableCell className="font-medium text-gray-900">
                  {ticket.customer_name}
                </TableCell>
                <TableCell>
                  <Badge color={CHANNEL_COLORS[ticket.channel]}>
                    {CHANNEL_LABELS[ticket.channel]}
                  </Badge>
                </TableCell>
                <TableCell>{ticket.subject}</TableCell>
                <TableCell>
                  <Badge color={STATUS_COLORS[ticket.status]} className="w-fit">
                    {STATUS_LABELS[ticket.status]}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge
                    color={PRIORITY_COLORS[ticket.priority]}
                    className="w-fit"
                  >
                    {PRIORITY_LABELS[ticket.priority]}
                  </Badge>
                </TableCell>
                <TableCell>
                  <a
                    href={`/tickets/${ticket.id}`}
                    className="font-medium text-blue-600 hover:underline"
                  >
                    Ver detalhes
                  </a>
                </TableCell>
              </TableRow>
            ))}

            {filteredTickets.length === 0 && (
              <TableRow>
                <TableCell
                  colSpan={6}
                  className="py-6 text-center text-gray-500"
                >
                  Nenhum ticket encontrado.
                </TableCell>
                z
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
