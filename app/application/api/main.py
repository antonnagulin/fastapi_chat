from fastapi import FastAPI

from application.api.massages.handlers import router as massage_router


def create_app()-> FastAPI:
    app = FastAPI(
        title="Simple Kafka chat",
        docs_url="/api/docs",
        description="Simple kafka + ddd example.",
        debug=True,
    )
    app.include_router(massage_router, prefix='/chat')
    return app