from datetime import date

from pydantic import BaseModel, ConfigDict


class DateRangeSchema(BaseModel):
    start: date
    end: date


class MetricsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date_range: DateRangeSchema
    total_records: int
    total_revenue_usd: float
    total_units_sold: int
    revenue_by_gpu_family: dict[str, float]
    revenue_by_region: dict[str, float]
    revenue_by_sales_channel: dict[str, float]
    revenue_by_customer_segment: dict[str, float]
    revenue_by_gpu_model: dict[str, float]
    monthly_revenue_trend: dict[str, float]
