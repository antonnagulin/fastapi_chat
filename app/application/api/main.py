from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="Simple Kafka chat",
        docs_url="/api/docs",
        description="Simple kafka + ddd example.",
        debug=True,
    )
