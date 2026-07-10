from fastapi import FastAPI

from app.shared.api.lifespan import lifespan
from app.shared.api.middleware import setup_middleware, setup_routes

app = FastAPI(
    debug=True,
    title="Desafio Stalse API",
    description="API para o desafio Stalse",
    version="0.0.1",
    lifespan=lifespan,
)

setup_middleware(app)
setup_routes(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
