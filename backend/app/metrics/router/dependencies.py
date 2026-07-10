from typing import Annotated

from fastapi import Depends

from ..service.metrics_service import MetricsService


def get_metrics_service() -> MetricsService:
    return MetricsService()


ServiceMetricsDep = Annotated[MetricsService, Depends(get_metrics_service)]
