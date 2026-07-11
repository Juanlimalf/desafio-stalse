"use client";

import { Button } from "flowbite-react";
import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center gap-6 px-4 py-16 text-center">
      <Image
        src="/system-error-concept.png"
        alt="Ilustração de erro de sistema"
        width={400}
        height={400}
        priority
      />
      <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
        404 - Página não encontrada
      </h1>
      <p className="text-lg text-gray-700 dark:text-gray-300">
        A página que você está procurando não existe.
      </p>
      <Button as={Link} href="/">
        Voltar para a home
      </Button>
    </div>
  );
}
