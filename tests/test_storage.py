import pytest
import json
import os
from src.storage import JSONStorage
from src.vacancy import Vacancy

@pytest.fixture
def test_file():
    """Фикстура для создания временного тестового файла"""
    file_path = "test_vacancies.json"
    yield file_path
    # Очистка после тестов
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.fixture
def sample_vacancy():
    """Фикстура для создания тестовой вакансии"""
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет"
    )

def test_storage_initialization(test_file):
    """Тест инициализации хранилища"""
    storage = JSONStorage(test_file)
    assert os.path.exists(test_file)
    
    # Проверка содержимого файла
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 0

def test_get_vacancies(test_file, sample_vacancy):
    """Тест получения вакансий"""
    storage = JSONStorage(test_file)
    storage.add_vacancy(sample_vacancy)
    
    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == sample_vacancy.title
    assert vacancies[0].url == sample_vacancy.url
    assert vacancies[0].salary_from == sample_vacancy.salary_from
    assert vacancies[0].salary_to == sample_vacancy.salary_to
    assert vacancies[0].salary_currency == sample_vacancy.salary_currency
    assert vacancies[0].description == sample_vacancy.description
    assert vacancies[0].requirements == sample_vacancy.requirements

def test_delete_vacancy(test_file, sample_vacancy):
    """Тест удаления вакансии"""
    storage = JSONStorage(test_file)
    storage.add_vacancy(sample_vacancy)
    
    # Проверка, что вакансия добавлена
    assert len(storage.get_vacancies()) == 1
    
    # Удаление вакансии
    storage.delete_vacancy(sample_vacancy)
    
    # Проверка, что вакансия удалена
    assert len(storage.get_vacancies()) == 0

def test_multiple_vacancies(test_file):
    """Тест работы с несколькими вакансиями"""
    storage = JSONStorage(test_file)
    
    # Создание нескольких вакансий
    vacancies = [
        Vacancy(
            title=f"Python Developer {i}",
            url=f"https://hh.ru/vacancy/{i}",
            salary={"from": 100000 + i * 10000, "to": 150000 + i * 10000, "currency": "RUR"},
            description=f"Разработка на Python {i}",
            requirements=f"Опыт работы от {i} лет"
        )
        for i in range(3)
    ]
    
    # Добавление вакансий
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)
    
    # Проверка получения всех вакансий
    stored_vacancies = storage.get_vacancies()
    assert len(stored_vacancies) == 3
    
    # Проверка содержимого каждой вакансии
    for i, vacancy in enumerate(stored_vacancies):
        assert vacancy.title == f"Python Developer {i}"
        assert vacancy.url == f"https://hh.ru/vacancy/{i}"
        assert vacancy.salary_from == 100000 + i * 10000
        assert vacancy.salary_to == 150000 + i * 10000
        assert vacancy.salary_currency == "RUR"
        assert vacancy.description == f"Разработка на Python {i}"
        assert vacancy.requirements == f"Опыт работы от {i} лет"

def test_duplicate_vacancies(test_file, sample_vacancy):
    """Тест предотвращения дублирования вакансий"""
    storage = JSONStorage(test_file)
    
    # Добавляем вакансию первый раз
    storage.add_vacancy(sample_vacancy)
    assert len(storage.get_vacancies()) == 1
    
    # Пытаемся добавить ту же вакансию снова
    storage.add_vacancy(sample_vacancy)
    assert len(storage.get_vacancies()) == 1  # Количество вакансий не должно измениться
    
    # Проверяем, что в файле тоже только одна вакансия
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert len(data) == 1 