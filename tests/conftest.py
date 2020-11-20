import pytest
from .test_processes.wps_test_collect_args import TestCollectArgs
from .test_processes.wps_test_process import TestProcess


@pytest.fixture
def mock_local_url(monkeypatch):
    monkeypatch.setenv("LOCAL_URL", "http://localhost:5000/wps")


@pytest.fixture
def mock_dev_url(monkeypatch):
    monkeypatch.setenv("DEV_URL", "http://docker-dev03.pcic.uvic.ca/somebird")


@pytest.fixture
def wps_test_collect_args(monkeypatch):
    return TestCollectArgs()


@pytest.fixture
def wps_test_process(monkeypatch):
    return TestProcess()
