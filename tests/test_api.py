import pytest
from unittest.mock import patch, MagicMock
from src.api import HeadHunterAPI

@pytest.fixture
def mock_response():
    """Фикстура для создания мока ответа API"""
    mock = MagicMock()
    mock.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Разработка на Python",
                "snippet": {"requirement": "Опыт работы от 3 лет"}
            }
        ]
    }
    return mock

def test_get_vacancies_success(mock_response):
    """Тест успешного получения вакансий"""
    with patch('requests.get', return_value=mock_response):
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python Developer")
        
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[0]["alternate_url"] == "https://hh.ru/vacancy/123"
        assert vacancies[0]["salary"]["from"] == 100000
        assert vacancies[0]["salary"]["to"] == 150000
        assert vacancies[0]["salary"]["currency"] == "RUR"
        assert vacancies[0]["description"] == "Разработка на Python"
        assert vacancies[0]["snippet"]["requirement"] == "Опыт работы от 3 лет"

def test_get_vacancies_empty_response():
    """Тест получения пустого ответа от API"""
    mock_empty = MagicMock()
    mock_empty.json.return_value = {"items": []}
    
    with patch('requests.get', return_value=mock_empty):
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python Developer")
        assert len(vacancies) == 0

def test_api_headers():
    """Тест заголовков запроса к API"""
    with patch('requests.get') as mock_get:
        api = HeadHunterAPI()
        api.get_vacancies("Python Developer")
        
        # Проверка заголовков запроса
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "User-Agent" in call_args[1]["headers"]
        assert "Mozilla/5.0" in call_args[1]["headers"]["User-Agent"]

def test_api_params():
    """Тест параметров запроса к API"""
    with patch('requests.get') as mock_get:
        api = HeadHunterAPI()
        search_query = "Python Developer"
        api.get_vacancies(search_query)
        
        # Проверка параметров запроса
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"]["text"] == search_query
        assert call_args[1]["params"]["area"] == 1
        assert call_args[1]["params"]["per_page"] == 100 