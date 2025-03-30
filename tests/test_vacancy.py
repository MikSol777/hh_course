import pytest
from src.vacancy import Vacancy

def test_vacancy_creation():
    """Тест создания вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет"
    )
    
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.salary_currency == "RUR"
    assert vacancy.description == "Разработка на Python"
    assert vacancy.requirements == "Опыт работы от 3 лет"

def test_vacancy_without_salary():
    """Тест создания вакансии без зарплаты"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary=None,
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет"
    )
    
    assert vacancy.salary_from is None
    assert vacancy.salary_to is None
    assert vacancy.salary_currency == "RUR"

def test_vacancy_comparison():
    """Тест сравнения вакансий"""
    vacancy1 = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет"
    )
    
    vacancy2 = Vacancy(
        title="Senior Python Developer",
        url="https://hh.ru/vacancy/124",
        salary={"from": 150000, "to": 200000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы от 5 лет"
    )
    
    vacancy3 = Vacancy(
        title="Junior Python Developer",
        url="https://hh.ru/vacancy/125",
        salary=None,
        description="Разработка на Python",
        requirements="Опыт работы от 1 года"
    )
    
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy3 < vacancy1
    assert vacancy3 < vacancy2

def test_vacancy_from_dict():
    """Тест создания вакансии из словаря"""
    vacancy_data = {
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "description": "Разработка на Python",
        "snippet": {"requirement": "Опыт работы от 3 лет"}
    }
    
    vacancy = Vacancy.from_dict(vacancy_data)
    
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.salary_currency == "RUR"
    assert vacancy.description == "Разработка на Python"
    assert vacancy.requirements == "Опыт работы от 3 лет"

def test_vacancy_validation():
    """Тест валидации данных вакансии"""
    with pytest.raises(ValueError, match="Название не может быть пустым"):
        Vacancy(
            title="",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python",
            requirements="Опыт работы от 3 лет"
        )
    
    with pytest.raises(ValueError, match="URL не может быть пустым"):
        Vacancy(
            title="Python Developer",
            url="",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python",
            requirements="Опыт работы от 3 лет"
        ) 