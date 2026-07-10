from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.metrics import router as metrics_router
from app.tickets import router as tickets_router


def setup_routes(app: FastAPI) -> None:
    app.include_router(tickets_router)
    app.include_router(metrics_router)


def setup_middleware(app: FastAPI) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
