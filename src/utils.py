import json
import os
from typing import List, Dict, Any
from .vacancy import Vacancy

def load_vacancies(file_path: str) -> List[Dict[str, Any]]:
    """
    Загрузка вакансий из JSON файла. Создает файл, если он не существует.
    
    Args:
        file_path (str): Путь к файлу
        
    Returns:
        List[Dict[str, Any]]: Список вакансий
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Создаем пустой файл, если он не существует
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

def save_vacancies(file_path: str, vacancies: List[Dict[str, Any]]) -> None:
    """
    Сохранение вакансий в JSON файл
    
    Args:
        file_path (str): Путь к файлу
        vacancies (List[Dict[str, Any]]): Список вакансий для сохранения
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=2)

def vacancy_to_dict(vacancy: Vacancy) -> Dict[str, Any]:
    """
    Преобразование объекта Vacancy в словарь
    
    Args:
        vacancy (Vacancy): Объект вакансии
        
    Returns:
        Dict[str, Any]: Словарь с данными вакансии
    """
    return {
        "name": vacancy.title,
        "alternate_url": vacancy.url,
        "salary": vacancy.salary,
        "description": vacancy.description,
        "snippet": {
            "requirement": vacancy.requirements
        }
    }

def dict_to_vacancy(data: Dict[str, Any]) -> Vacancy:
    """
    Преобразование словаря в объект Vacancy
    
    Args:
        data (Dict[str, Any]): Словарь с данными вакансии
        
    Returns:
        Vacancy: Объект вакансии
    """
    return Vacancy(
        title=data["name"],
        url=data["alternate_url"],
        salary=data["salary"],
        description=data["description"],
        requirements=data["snippet"]["requirement"]
    ) 