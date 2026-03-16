import requests
from requests import Response
from typing import Dict, Optional, Any


class AviasalesClient:
    """Класс для взаимодействия с API Aviasales (Travelpayouts)."""

    def __init__(self, token: str) -> None:
        """Инициализирует клиент API.

        Args:
            token (str): Токен доступа к API (X-Access-Token).
        """
        self.base_url = "https://api.travelpayouts.com/aviasales/v3/"
        self.token = token

    def _get_default_headers(self) -> Dict[str, str]:
        """Возвращает заголовки по умолчанию, включая токен."""
        return {"X-Access-Token": self.token}

    def get_prices_for_dates(self, params: Optional[Dict[str, Any]] = None, 
                             headers: Optional[Dict[str, str]] = None) -> Response:
        """Выполняет GET-запрос к эндпоинту prices_for_dates.

        Args:
            params (dict, optional): Параметры строки запроса.
            headers (dict, optional): Заголовки запроса. Если None, используется токен по умолчанию.

        Returns:
            Response: Объект ответа библиотеки requests.
        """
        url = f"{self.base_url}prices_for_dates"
        req_headers = headers if headers is not None else self._get_default_headers()
        return requests.get(url, params=params, headers=req_headers)

    def post_prices_for_dates(self, params: Optional[Dict[str, Any]] = None) -> Response:
        """Выполняет POST-запрос к эндпоинту prices_for_dates (для проверки негативных сценариев).

        Args:
            params (dict, optional): Параметры строки запроса.

        Returns:
            Response: Объект ответа библиотеки requests.
        """
        url = f"{self.base_url}prices_for_dates"
        return requests.post(url, params=params, headers=self._get_default_headers())
