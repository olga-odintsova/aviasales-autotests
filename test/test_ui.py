import pytest
import allure
from selenium import webdriver
from pages.SearchPage import SearchPage
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture
def driver():
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


@pytest.mark.ui
@allure.story("Aviasales UI")
@allure.title("Поиск по полному названию города")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_full_city_name(driver):
    page = SearchPage(driver)
    search_query = "Москва"
    
    with allure.step("Открытие страницы"):
        page.open()
        
    with allure.step(f"Ввод названия города '{search_query}'"):
        page.enter_search_query(search_query)
        
    with allure.step("Проверка появления релевантных подсказок и выбор города"):
        items = page.get_dropdown_items_text()
        assert len(items) > 0, "Выпадающий список пуст"
        page.select_dropdown_item_by_text(search_query)
        
    with allure.step("Проверка, что город корректно заполнился в поле"):
        assert search_query.lower() in page.get_input_value().lower()

@pytest.mark.ui
@allure.story("Aviasales UI")
@allure.title("Поиск по IATA коду аэропорта")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_iata_code(driver):
    page = SearchPage(driver)
    
    with allure.step("Открытие страницы"):
        page.open()
        
    with allure.step("Ввод IATA кода 'SVO'"):
        page.enter_search_query("SVO")
        
    with allure.step("Выбор аэропорта 'Шереметьево' из подсказок"):
        page.select_dropdown_item_by_text("Шереметьево")
        
    with allure.step("Проверка, что поле заполнено корректно"):
        assert "Шереметьево" in page.get_input_value()

@pytest.mark.ui
@allure.story("Aviasales UI")
@allure.title("Поиск по названию страны")
@allure.severity(allure.severity_level.NORMAL)
def test_search_country_name(driver):
    page = SearchPage(driver)
    
    with allure.step("Открытие страницы"):
        page.open()
        
    with allure.step("Ввод названия страны 'Италия'"):
        page.enter_search_query("Италия")
        
    with allure.step("Выбор конкретного аэропорта (например, Рим) из списка"):
        page.select_dropdown_item_by_text("Рим")
        
    with allure.step("Проверка, что выбран нужный город/аэропорт"):
        assert "Рим" in page.get_input_value()

@pytest.mark.ui
@allure.story("Aviasales UI")
@allure.title("Ввод части названия города")
@allure.severity(allure.severity_level.NORMAL)
def test_search_partial_country_name(driver):
    page = SearchPage(driver)
    search_query = "Лондон"
    
    with allure.step("Открытие страницы"):
        page.open()
        
    with allure.step(f"Ввод названия города '{search_query}'"):
        page.enter_search_query(search_query[:4])
        
    with allure.step("Проверка появления релевантных подсказок и выбор города"):
        items = page.get_dropdown_items_text()
        assert len(items) > 0, "Выпадающий список пуст"
        page.select_dropdown_item_by_text(search_query)
        
    with allure.step("Проверка, что город корректно заполнился в поле"):
        assert search_query.lower() in page.get_input_value().lower()

# ================= НЕГАТИВНЫЕ СЦЕНАРИИ =================

@pytest.mark.ui
@allure.story("Aviasales UI")
@allure.title("Ввод несуществующего названия")
@allure.severity(allure.severity_level.NORMAL)
def test_search_invalid_name(driver):
    page = SearchPage(driver)
    
    with allure.step("Открытие страницы"):
        page.open()
        
    with allure.step("Ввод несуществующего значения 'Абвгдейка'"):
        page.enter_search_query("Абвгдейка")
        
    with allure.step("Проверка отображения сообщения 'Ничего не найдено' или пустого списка"):
        items = page.get_dropdown_items_text()
        empty_msg = page.get_empty_result_message()
        
        # Проверяем, что либо список пуст, либо появилось сообщение об ошибке
        assert len(items) == 0 or empty_msg != "", "Должно появиться сообщение об ошибке или пустой список"

