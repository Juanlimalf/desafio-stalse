"use client";

import { ticketsService } from "@/modules/services/TicketsService";
import { Button, Modal, ModalBody, ModalHeader, TextInput } from "flowbite-react";
import { useEffect, useState } from "react";

type Props = {
  open: boolean;
  currentUrl: string;
  onClose: () => void;
  onSaved: (url: string) => void;
};

export function WebhookUpdateModal({
  open,
  currentUrl,
  onClose,
  onSaved,
}: Readonly<Props>) {
  const [newUrl, setNewUrl] = useState(currentUrl);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) setNewUrl(currentUrl);
  }, [open, currentUrl]);

  async function handleSave() {
    setSaving(true);

    try {
      await ticketsService.modifyWebhook(newUrl);
      onSaved(newUrl);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal show={open} onClose={onClose}>
      <ModalHeader>Atualizar webhook</ModalHeader>
      <ModalBody>
        <div className="flex flex-col gap-4">
          <TextInput
            placeholder="https://exemplo.com/webhook"
            value={newUrl}
            onChange={(event) => setNewUrl(event.target.value)}
          />
          <div className="flex justify-end gap-2">
            <Button onClick={onClose} color="gray" className="mr-2">
              Cancelar
            </Button>

            <Button onClick={handleSave} disabled={saving}>
              {saving ? "Salvando..." : "Salvar"}
            </Button>
          </div>
        </div>
      </ModalBody>
    </Modal>
  );
}
