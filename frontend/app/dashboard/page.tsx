import { metricsService } from "@/modules/services/MetricsService";
import { Card } from "flowbite-react";
import { BackButton } from "../tickets/components/BackButton";
import { DashboardCharts } from "./components/DashboardCharts";

const numberFormatter = new Intl.NumberFormat("pt-BR");

const dateFormatter = new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" });

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "USD",
});

export default async function DashboardPage() {
  const metrics = await metricsService.getMetrics();

  return (
    <main className="flex min-h-screen flex-col items-center px-4 py-12">
      <div className="w-full max-w-6xl">
        <BackButton />
      </div>
      <div className="w-full max-w-6xl">
        <h1 className="mb-6 text-2xl font-bold text-gray-900">Dashboard</h1>
        <h3 className="mb-6 text-2xl font-bold text-gray-900">
          Periodo {dateFormatter.format(new Date(metrics.date_range.start))} -{" "}
          {dateFormatter.format(new Date(metrics.date_range.end))}
        </h3>

        <div className="mb-8 grid grid-cols-3 gap-4">
          <Card>
            <p className="text-sm text-gray-500">Total de registros</p>
            <p className="text-2xl font-bold text-gray-900">
              {numberFormatter.format(metrics.total_records)}
            </p>
          </Card>

          <Card>
            <p className="text-sm text-gray-500">Receita total</p>
            <p className="text-2xl font-bold text-gray-900">
              {currencyFormatter.format(metrics.total_revenue_usd)}
            </p>
          </Card>

          <Card>
            <p className="text-sm text-gray-500">Unidades vendidas</p>
            <p className="text-2xl font-bold text-gray-900">
              {numberFormatter.format(metrics.total_units_sold)}
            </p>
          </Card>
        </div>

        <DashboardCharts metrics={metrics} />
      </div>
    </main>
  );
}
