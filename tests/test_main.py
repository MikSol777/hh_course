import pytest
from src.vacancy import Vacancy
from main import filter_vacancies_by_keyword, get_top_vacancies

@pytest.fixture
def sample_vacancies():
    """Фикстура для создания тестовых вакансий"""
    return [
        Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python и Django",
            requirements="Опыт работы от 3 лет, Python, Django"
        ),
        Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/124",
            salary={"from": 150000, "to": 200000, "currency": "RUR"},
            description="Разработка на Java и Spring",
            requirements="Опыт работы от 3 лет, Java, Spring"
        ),
        Vacancy(
            title="Frontend Developer",
            url="https://hh.ru/vacancy/125",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            description="Разработка на React и TypeScript",
            requirements="Опыт работы от 3 лет, React, TypeScript"
        )
    ]

def test_filter_vacancies_by_keyword(sample_vacancies):
    """Тест фильтрации вакансий по ключевому слову"""
    # Поиск по Python
    python_vacancies = filter_vacancies_by_keyword(sample_vacancies, "Python")
    assert len(python_vacancies) == 1
    assert python_vacancies[0].title == "Python Developer"
    
    # Поиск по React
    react_vacancies = filter_vacancies_by_keyword(sample_vacancies, "React")
    assert len(react_vacancies) == 1
    assert react_vacancies[0].title == "Frontend Developer"
    
    # Поиск по опыту работы
    experience_vacancies = filter_vacancies_by_keyword(sample_vacancies, "опыт работы")
    assert len(experience_vacancies) == 3
    
    # Поиск с учетом регистра
    python_vacancies_upper = filter_vacancies_by_keyword(sample_vacancies, "PYTHON")
    assert len(python_vacancies_upper) == 1
    assert python_vacancies_upper[0].title == "Python Developer"
    
    # Поиск несуществующего ключевого слова
    no_vacancies = filter_vacancies_by_keyword(sample_vacancies, "PHP")
    assert len(no_vacancies) == 0

def test_get_top_vacancies(sample_vacancies):
    """Тест получения топ N вакансий по зарплате"""
    # Получение топ 2 вакансий
    top_2 = get_top_vacancies(sample_vacancies, 2)
    assert len(top_2) == 2
    assert top_2[0].title == "Java Developer"  # 150000
    assert top_2[1].title == "Frontend Developer"  # 120000
    
    # Получение топ 1 вакансии
    top_1 = get_top_vacancies(sample_vacancies, 1)
    assert len(top_1) == 1
    assert top_1[0].title == "Java Developer"
    
    # Получение топ N вакансий, где N больше количества вакансий
    top_all = get_top_vacancies(sample_vacancies, 5)
    assert len(top_all) == 3
    assert top_all[0].title == "Java Developer"
    assert top_all[1].title == "Frontend Developer"
    assert top_all[2].title == "Python Developer"

def test_get_top_vacancies_with_none_salary():
    """Тест получения топ N вакансий с учетом вакансий без зарплаты"""
    vacancies = [
        Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработка на Python",
            requirements="Опыт работы от 3 лет"
        ),
        Vacancy(
            title="Java Developer",
            url="https://hh.ru/vacancy/124",
            salary=None,
            description="Разработка на Java",
            requirements="Опыт работы от 3 лет"
        ),
        Vacancy(
            title="Frontend Developer",
            url="https://hh.ru/vacancy/125",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            description="Разработка на React",
            requirements="Опыт работы от 3 лет"
        )
    ]
    
    top_2 = get_top_vacancies(vacancies, 2)
    assert len(top_2) == 2
    assert top_2[0].title == "Frontend Developer"
    assert top_2[1].title == "Python Developer" 