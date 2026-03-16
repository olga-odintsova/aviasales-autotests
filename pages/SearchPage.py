from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List


class SearchPage:
    """Класс Page Object для взаимодействия с полем поиска городов/аэропортов."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализирует класс страницы поиска.

        Args:
            driver (WebDriver): Экземпляр веб-драйвера Selenium.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

        self.input_locator = (By.ID, 'avia_form_destination-input')
        self.dropdown_item_locator = (By.ID, 'avia_form_destination-menu')
        self.empty_result_locator = (By.CSS_SELECTOR, '[data-test-id="status-message"]')

    def open(self) -> None:
        """Открывает главную страницу поиска."""
        self.driver.get("https://www.aviasales.ru/")  # Укажите нужный URL

    def enter_search_query(self, query: str) -> None:
        """Вводит текст в поле поиска.

        Args:
            query (str): Поисковый запрос.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.input_locator))
        element.clear()
        element.send_keys(query)

    def get_dropdown_items_text(self) -> List[str]:
        """Возвращает список текстов из всех элементов выпадающего списка."""
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self.dropdown_item_locator))
            return [item.text for item in items]
        except Exception:
            # Если список не появился или пуст по таймауту
            return []

    def select_dropdown_item_by_text(self, target_text: str) -> None:
        """Ищет элемент в дропдауне по частичному совпадению текста и кликает по нему.

        Args:
            target_text (str): Текст (или часть текста), который должен быть в элементе.
        """

        self.wait.until(EC.text_to_be_present_in_element(self.dropdown_item_locator, target_text))
        items = self.wait.until(EC.presence_of_all_elements_located(self.dropdown_item_locator))

        for item in items[0].find_elements(By.XPATH, './*'):
            if target_text.lower() in item.text.lower():
                item.click()
                return
        raise AssertionError(f"Элемент с текстом '{target_text}' не найден в выпадающем списке")

    def get_input_value(self) -> str:
        """Возвращает текущее значение, введенное в поле поиска."""
        element = self.wait.until(EC.presence_of_element_located(self.input_locator))
        return element.get_attribute('value')

    def get_empty_result_message(self) -> str:
        """Возвращает текст сообщения о том, что ничего не найдено."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.empty_result_locator))
            return element.text
        except Exception:
            return ""
