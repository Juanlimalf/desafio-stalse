from pathlib import Path

from fastapi import HTTPException, status

from app.metrics.schema.metrics_schema import MetricsSchema
from app.shared.log.logger import logger

base_dir = Path(__file__).resolve().parents[4] / "data/processed"


class MetricsService:
    async def get_metrics(self) -> MetricsSchema:
        try:
            metrics_file_path = base_dir / "metrics.json"

            if not metrics_file_path.exists():
                raise FileNotFoundError(f"Metrics file not found at {metrics_file_path}")

            metrics_data = metrics_file_path.read_text(encoding="utf-8")

            return MetricsSchema.model_validate_json(metrics_data)

        except FileNotFoundError as e:
            logger.error(f"Metrics file not found: {e!s}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Metrics file not found: {e!s}",
            ) from e

        except Exception as e:
            logger.exception("Error reading metrics file")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading metrics: {e!s}",
            ) from e
