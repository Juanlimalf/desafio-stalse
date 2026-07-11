import { Card } from "flowbite-react";
import Link from "next/link";

export default async function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-start px-4 py-24">
      <div className="relative flex w-full max-w-5xl flex-col items-center justify-center gap-12">
        <h1 className="text-2xl font-bold text-gray-900">Painel</h1>

        <div className="grid w-full max-w-2xl grid-cols-1 gap-6 sm:grid-cols-2">
          <Link href="/tickets">
            <Card className="h-full transition hover:shadow-lg">
              <h2 className="text-xl font-bold text-gray-900">Tickets</h2>
              <p className="text-gray-500">
                Veja e gerencie os tickets recebidos.
              </p>
            </Card>
          </Link>

          <Link href="/dashboard">
            <Card className="h-full transition hover:shadow-lg">
              <h2 className="text-xl font-bold text-gray-900">Dashboard</h2>
              <p className="text-gray-500">Acompanhe métricas e indicadores.</p>
            </Card>
          </Link>
        </div>
      </div>
    </main>
  );
}
