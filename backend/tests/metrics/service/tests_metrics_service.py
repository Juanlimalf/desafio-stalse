import asyncio
from pathlib import Path

import pytest
from fastapi import HTTPException

import app.metrics.service.metrics_service as metrics_service_module
from app.metrics.schema.metrics_schema import MetricsSchema
from app.metrics.service.metrics_service import MetricsService

VALID_METRICS_JSON = """{
    "date_range": {"start": "2026-01-01", "end": "2026-01-31"},
    "total_records": 10,
    "total_revenue_usd": 100.0,
    "total_units_sold": 5,
    "revenue_by_gpu_family": {"RTX": 100.0},
    "revenue_by_region": {"US": 100.0},
    "revenue_by_sales_channel": {"Online": 100.0},
    "revenue_by_customer_segment": {"Consumer": 100.0},
    "revenue_by_gpu_model": {"4090": 100.0},
    "monthly_revenue_trend": {"2026-01": 100.0}
}"""


class TestMetricsService:
    def setup_method(self) -> None:
        self.service = MetricsService()

    def test_get_metrics_returns_schema_when_file_exists(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        (tmp_path / "metrics.json").write_text(VALID_METRICS_JSON, encoding="utf-8")
        monkeypatch.setattr(metrics_service_module, "base_dir", tmp_path)

        result = asyncio.run(self.service.get_metrics())

        assert isinstance(result, MetricsSchema)
        assert result.total_records == 10

    def test_get_metrics_raises_404_when_file_not_found(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(metrics_service_module, "base_dir", tmp_path)

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.get_metrics())

        assert exc_info.value.status_code == 404

    def test_get_metrics_raises_500_on_invalid_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        (tmp_path / "metrics.json").write_text("not valid json", encoding="utf-8")
        monkeypatch.setattr(metrics_service_module, "base_dir", tmp_path)

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(self.service.get_metrics())

        assert exc_info.value.status_code == 500
