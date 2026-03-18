import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pages.AviasalesClient import AviasalesClient

# ================= ФИКСТУРЫ ДЛЯ API =================


@pytest.fixture
def api_client() -> AviasalesClient:
    """Фикстура для инициализации клиента API перед каждым тестом."""
    return AviasalesClient(os.environ["TOKEN"])


@pytest.fixture
def base_params() -> dict:
    """Фикстура с базовыми параметрами для успешного запроса."""
    return {
        "origin": "TBS",
        "destination": "MOW",
        "departure_at": "2026-01",
        "return_at": "2026-02",
        "unique": "false",
        "sorting": "price",
        "direct": "false",
        "currency": "rub",
        "limit": "30",
        "page": "1",
        "one_way": "false"
    }

# ================= ФИКСТУРЫ ДЛЯ UI =================


@pytest.fixture
def driver():
    """Фикстура для инициализации веб-драйвера Edge."""
    url = "https://msedgedriver.microsoft.com/LATEST_RELEASE"
    driver = webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager(
            url="https://msedgedriver.microsoft.com",
            latest_release_url=url).install())
    )
    driver.implicitly_wait(3)
    driver.maximize_window()
    yield driver
    driver.quit()
