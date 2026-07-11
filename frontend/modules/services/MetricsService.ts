import type { Metrics } from "@/modules/interfaces/Metrics";

class MetricsService {
  private readonly baseUrl = `${process.env.BACKEND_URL ?? "http://127.0.0.1:8000"}/metrics/`;

  async getMetrics(): Promise<Metrics> {
    const response = await fetch(this.baseUrl);

    if (!response.ok) throw new Error("Failed to fetch metrics");

    return response.json();
  }
}

export const metricsService = new MetricsService();
