"use client";

import { useRouter } from "next/navigation";

export function BackButton() {
  const router = useRouter();

  return (
    <button
      type="button"
      onClick={() => router.back()}
      className="mb-4 inline-block text-sm font-medium text-blue-600 hover:underline"
    >
      &larr; Voltar
    </button>
  );
}
