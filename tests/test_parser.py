import pytest
from src.parser import HeadHunterParser
from src.vacancy import Vacancy

def test_parse_vacancies():
    """Тест парсинга вакансий"""
    parser = HeadHunterParser()
    
    vacancies_data = [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "description": "Разработка на Python",
            "snippet": {"requirement": "Опыт работы от 3 лет"}
        },
        {
            "name": "Senior Python Developer",
            "alternate_url": "https://hh.ru/vacancy/124",
            "salary": None,
            "description": "Разработка на Python",
            "snippet": {"requirement": "Опыт работы от 5 лет"}
        }
    ]
    
    vacancies = parser.parse_vacancies(vacancies_data)
    
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert isinstance(vacancies[1], Vacancy)
    
    # Проверка первой вакансии
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].url == "https://hh.ru/vacancy/123"
    assert vacancies[0].salary_from == 100000
    assert vacancies[0].salary_to == 150000
    assert vacancies[0].salary_currency == "RUR"
    assert vacancies[0].description == "Разработка на Python"
    assert vacancies[0].requirements == "Опыт работы от 3 лет"
    
    # Проверка второй вакансии
    assert vacancies[1].title == "Senior Python Developer"
    assert vacancies[1].url == "https://hh.ru/vacancy/124"
    assert vacancies[1].salary_from is None
    assert vacancies[1].salary_to is None
    assert vacancies[1].salary_currency == "RUR"
    assert vacancies[1].description == "Разработка на Python"
    assert vacancies[1].requirements == "Опыт работы от 5 лет"

def test_parse_empty_vacancies():
    """Тест парсинга пустого списка вакансий"""
    parser = HeadHunterParser()
    vacancies = parser.parse_vacancies([])
    assert len(vacancies) == 0
    assert isinstance(vacancies, list) 