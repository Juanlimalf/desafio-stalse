"""Transforma o CSV bruto de vendas de GPU em um JSON de metricas agregadas."""

import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
RAW_CSV = BASE_DIR / "raw" / "nvidia_gpu_sales_synthetic_2026.csv"
OUTPUT_JSON = BASE_DIR / "processed" / "metrics.json"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_CSV)

    df["sale_date"] = pd.to_datetime(df["sale_date"])

    return df


def build_metrics(df: pd.DataFrame) -> dict:

    date_range = {
        "start": df["sale_date"].min().strftime("%Y-%m-%d"),
        "end": df["sale_date"].max().strftime("%Y-%m-%d"),
    }
    total_revenue_usd = round(df["revenue_usd"].sum(), 2)
    total_units_sold = df["units_sold"].sum()

    revenue_by_gpu_family = df.groupby("gpu_family")["revenue_usd"].sum().round(2).to_dict()
    revenue_by_region = df.groupby("region")["revenue_usd"].sum().sort_values(ascending=False).round(2).to_dict()
    revenue_by_sales_channel = df.groupby("sales_channel")["revenue_usd"].sum().sort_values(ascending=False).round(2).to_dict()
    revenue_by_customer_segment = df.groupby("customer_segment")["revenue_usd"].sum().sort_values(ascending=False).round(2).to_dict()
    revenue_by_gpu_model = df.groupby("gpu_model")["revenue_usd"].sum().sort_values(ascending=False).round(2).to_dict()

    monthly_revenue = df.set_index("sale_date").resample("MS")["revenue_usd"].sum()
    dict_monthly_revenue = {ts.strftime("%Y-%m"): round(v, 2) for ts, v in monthly_revenue.items()}

    return {
        "date_range": date_range,
        "total_records": len(df),
        "total_revenue_usd": total_revenue_usd,
        "total_units_sold": int(total_units_sold),
        "revenue_by_gpu_family": revenue_by_gpu_family,
        "revenue_by_region": revenue_by_region,
        "revenue_by_sales_channel": revenue_by_sales_channel,
        "revenue_by_customer_segment": revenue_by_customer_segment,
        "revenue_by_gpu_model": revenue_by_gpu_model,
        "monthly_revenue_trend": dict_monthly_revenue,
    }


def save_metrics(metrics: dict) -> None:

    if not OUTPUT_JSON.parent.exists():
        OUTPUT_JSON.parent.mkdir(parents=True)
    OUTPUT_JSON.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    df = load_data()

    metrics = build_metrics(df)

    save_metrics(metrics)


if __name__ == "__main__":
    main()
