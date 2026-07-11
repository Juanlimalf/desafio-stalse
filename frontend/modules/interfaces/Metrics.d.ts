export type DateRange = {
  start: string;
  end: string;
};

export type Metrics = {
  date_range: DateRange;
  total_records: number;
  total_revenue_usd: number;
  total_units_sold: number;
  revenue_by_gpu_family: Record<string, number>;
  revenue_by_region: Record<string, number>;
  revenue_by_sales_channel: Record<string, number>;
  revenue_by_customer_segment: Record<string, number>;
  revenue_by_gpu_model: Record<string, number>;
  monthly_revenue_trend: Record<string, number>;
};
