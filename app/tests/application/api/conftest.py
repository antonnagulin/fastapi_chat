import pytest
from application.api.main import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from logic.init import init_cotainer

from tests.fixtures import init_dummy_container


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_cotainer] = init_dummy_container
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
