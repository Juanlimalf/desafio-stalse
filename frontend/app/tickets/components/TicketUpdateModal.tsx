"use client";

import { TicketPriority, TicketStatus } from "@/modules/enum/TicketsEnum";
import type { Ticket } from "@/modules/interfaces/Tickets";
import {
  PRIORITY_LABELS,
  STATUS_LABELS,
} from "@/modules/mappers/TicketsMappers";
import { ticketsService } from "@/modules/services/TicketsService";
import {
  Button,
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader,
  Select,
} from "flowbite-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

type Props = {
  ticket: Ticket;
};

export function TicketUpdateModal({ ticket }: Readonly<Props>) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState(ticket.status);
  const [priority, setPriority] = useState(ticket.priority);

  const handleUpdate = async () => {
    try {
      await ticketsService.alterTicketStatusPriority(
        ticket.id,
        status,
        priority,
      );
      router.refresh();
    } finally {
      setOpen(false);
    }
  };

  return (
    <>
      <Button onClick={() => setOpen(true)}>Ver mais detalhes</Button>

      <Modal show={open} onClose={() => setOpen(false)}>
        <ModalHeader>Ticket {ticket.id}</ModalHeader>
        <ModalBody>
          <div className="flex flex-col gap-4">
            <Select
              value={status}
              onChange={(event) =>
                setStatus(event.target.value as TicketStatus)
              }
            >
              {Object.values(TicketStatus).map((value) => (
                <option key={value} value={value}>
                  {STATUS_LABELS[value]}
                </option>
              ))}
            </Select>
            <Select
              value={priority}
              onChange={(event) =>
                setPriority(event.target.value as TicketPriority)
              }
            >
              {Object.values(TicketPriority).map((value) => (
                <option key={value} value={value}>
                  {PRIORITY_LABELS[value]}
                </option>
              ))}
            </Select>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button onClick={() => setOpen(false)}>Fechar</Button>
          <Button onClick={handleUpdate}>Atualizar</Button>
        </ModalFooter>
      </Modal>
    </>
  );
}
