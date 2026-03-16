import pytest
import allure
from pages.AviasalesClient import AviasalesClient
import os


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


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Успешный запрос: цены на даты (туда-обратно, RUB)")
@allure.severity(allure.severity_level.CRITICAL)
def test_prices_two_way_rub(api_client, base_params):
    with allure.step("Отправка GET-запроса с корректными параметрами"):
        response = api_client.get_prices_for_dates(params=base_params)

    with allure.step("Проверка статус-кода (ожидается 200)"):
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Успешный запрос: цены на даты (в одну сторону)")
@allure.severity(allure.severity_level.CRITICAL)
def test_prices_one_way(api_client, base_params):
    params = base_params.copy()
    params["one_way"] = "true"
    del params["return_at"]  # При билете в одну сторону дата возврата не нужна

    with allure.step("Отправка GET-запроса (one_way=true)"):
        response = api_client.get_prices_for_dates(params=params)

    with allure.step("Проверка статус-кода (ожидается 200)"):
        assert response.status_code == 200


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Успешный запрос: цены на даты (валюта GEL)")
@allure.severity(allure.severity_level.NORMAL)
def test_prices_currency_gel(api_client, base_params):
    params = base_params.copy()
    params["currency"] = "gel"

    with allure.step("Отправка GET-запроса (currency=gel)"):
        response = api_client.get_prices_for_dates(params=params)

    with allure.step("Проверка статус-кода (ожидается 200)"):
        assert response.status_code == 200


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Негативный запрос: неверный код аэропорта")
@allure.severity(allure.severity_level.NORMAL)
def test_bad_airport(api_client, base_params):
    params = base_params.copy()
    params["origin"] = "XXX"

    with allure.step("Отправка запроса с несуществующим аэропортом отправления"):
        response = api_client.get_prices_for_dates(params=params)

    with allure.step("Проверка статус-кода (ожидается 400)"):
        assert response.status_code == 400


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Негативный запрос: пустой поиск (без параметров)")
@allure.severity(allure.severity_level.NORMAL)
def test_empty_search(api_client):
    with allure.step("Отправка GET-запроса без параметров"):
        response = api_client.get_prices_for_dates(params={})

    with allure.step("Проверка статус-кода (ожидается 400)"):
        assert response.status_code == 400


@pytest.mark.api
@allure.story("Aviasales API")
@allure.title("Негативный запрос: использование неверного HTTP-метода (POST)")
@allure.severity(allure.severity_level.NORMAL)
def test_wrong_method(api_client, base_params):
    with allure.step("Отправка POST-запроса вместо GET"):
        response = api_client.post_prices_for_dates(params=base_params)

    with allure.step("Проверка статус-кода (ожидается 404)"):
        assert response.status_code == 404


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Негативный запрос: без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_no_token(api_client, base_params):
    with allure.step("Отправка запроса без заголовка X-Access-Token"):
        # Передаем пустые заголовки
        response = api_client.get_prices_for_dates(params=base_params, headers={})

    with allure.step("Проверка статус-кода (ожидается 401)"):
        assert response.status_code == 401


@pytest.mark.api
@allure.story("Aviasales API: prices_for_dates")
@allure.title("Негативный запрос: неверный токен авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_wrong_token(api_client, base_params):
    with allure.step("Отправка запроса с невалидным токеном"):
        response = api_client.get_prices_for_dates(
            params=base_params,
            headers={"X-Access-Token": "WRONG_TOKEN"}
        )

    with allure.step("Проверка статус-кода (ожидается 401)"):
        assert response.status_code == 401
