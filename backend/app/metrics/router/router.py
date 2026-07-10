from fastapi import APIRouter

from app.metrics.router.dependencies import ServiceMetricsDep
from app.metrics.schema.metrics_schema import MetricsSchema

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/")
async def get_metrics(service: ServiceMetricsDep) -> MetricsSchema:
    """Busca as métricas do sistema apartir do arquivo metrics.json, que está na pasta data/processed."""

    return await service.get_metrics()
