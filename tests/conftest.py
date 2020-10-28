import pytest


@pytest.fixture
def mock_local_url(monkeypatch):
    monkeypatch.setenv("LOCAL_URL", "http://localhost:5000/wps")


@pytest.fixture
def mock_dev_url(monkeypatch):
    monkeypatch.setenv("DEV_URL", "http://docker-dev03.pcic.uvic.ca/somebird")
