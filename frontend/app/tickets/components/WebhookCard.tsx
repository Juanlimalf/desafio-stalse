"use client";

import { Button } from "flowbite-react";
import { useState } from "react";
import { WebhookUpdateModal } from "./WebhookUpdateModal";

type Props = {
  url: string;
};

export function WebhookCard({ url }: Readonly<Props>) {
  const [currentUrl, setCurrentUrl] = useState(url);
  const [open, setOpen] = useState(false);

  return (
    <div className="mb-6 flex items-center justify-between gap-4 rounded-lg border border-gray-200 bg-gray-50 px-4 py-3 dark:border-gray-700 dark:bg-gray-800">
      <div className="min-w-0">
        <p className="text-xs font-medium text-gray-500 uppercase dark:text-gray-400">
          Webhook
        </p>
        <p className="truncate text-sm text-gray-900 dark:text-white">
          {currentUrl || "Nenhuma URL cadastrada"}
        </p>
      </div>

      <Button size="sm" onClick={() => setOpen(true)}>
        Atualizar
      </Button>

      <WebhookUpdateModal
        open={open}
        currentUrl={currentUrl}
        onClose={() => setOpen(false)}
        onSaved={(newUrl) => {
          setCurrentUrl(newUrl);
          setOpen(false);
        }}
      />
    </div>
  );
}
