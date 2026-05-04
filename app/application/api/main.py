import asyncio
from contextlib import asynccontextmanager

from aiojobs import Scheduler
from fastapi import FastAPI
from logic.init import init_container
from punq import Container

from application.api.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)
from application.api.messages.handlers import router as message_router
from application.api.websockets.messages import router as message_ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()
    
    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)
    
    job = await scheduler.spawn(consume_in_background())
    
    yield 

    await close_message_broker()
    job.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple Kafka chat",
        docs_url="/api/docs",
        description="Simple kafka + ddd example.",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(message_router, prefix="/chats")
    app.include_router(message_ws_router, prefix="/chats")
    return app
