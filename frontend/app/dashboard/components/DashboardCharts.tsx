import type { Metrics } from "@/modules/interfaces/Metrics";
import { MonthlyRevenueTrendChart } from "./MonthlyRevenueTrendChart";
import { RevenueByCustomerSegmentChart } from "./RevenueByCustomerSegmentChart";
import { RevenueByGpuFamilyChart } from "./RevenueByGpuFamilyChart";
import { RevenueByGpuModelChart } from "./RevenueByGpuModelChart";
import { RevenueByRegionChart } from "./RevenueByRegionChart";
import { RevenueBySalesChannelChart } from "./RevenueBySalesChannelChart";

type Props = {
  metrics: Metrics;
};

export function DashboardCharts({ metrics }: Readonly<Props>) {
  return (
    <div className="grid grid-cols-1 gap-8 rounded-lg border border-gray-200 bg-white p-6 shadow">
      <MonthlyRevenueTrendChart data={metrics.monthly_revenue_trend} />
      <RevenueByGpuFamilyChart data={metrics.revenue_by_gpu_family} />
      <RevenueBySalesChannelChart data={metrics.revenue_by_sales_channel} />
      <RevenueByRegionChart data={metrics.revenue_by_region} />
      <RevenueByCustomerSegmentChart
        data={metrics.revenue_by_customer_segment}
      />
      <RevenueByGpuModelChart data={metrics.revenue_by_gpu_model} />
    </div>
  );
}
