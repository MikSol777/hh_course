from abc import ABC, abstractmethod
import json
from typing import List, Optional
from .vacancy import Vacancy
from .parser import HeadHunterParser

class VacancyStorage(ABC):
    """Абстрактный базовый класс для хранилища вакансий"""
    
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в хранилище"""
        pass
    
    @abstractmethod
    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """Получение вакансий из хранилища"""
        pass
    
    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из хранилища"""
        pass

class JSONStorage(VacancyStorage):
    """Реализация хранилища на основе JSON файла"""
    
    def __init__(self, file_path: str = "vacancies.json"):
        self.file_path = file_path
        self.parser = HeadHunterParser()
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Проверка существования JSON файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _read_vacancies(self) -> List[dict]:
        """Чтение вакансий из JSON файла"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_vacancies(self, vacancies: List[dict]) -> None:
        """Запись вакансий в JSON файл"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)
    
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в JSON хранилище"""
        vacancies = self._read_vacancies()
        vacancy_dict = {
            'name': vacancy.title,
            'alternate_url': vacancy.url,
            'salary': vacancy.salary,
            'description': vacancy.description,
            'snippet': {'requirement': vacancy.requirements}
        }
        vacancies.append(vacancy_dict)
        self._write_vacancies(vacancies)
    
    def get_vacancies(self, **kwargs) -> List[Vacancy]:
        """Получение вакансий из JSON хранилища"""
        vacancies_data = self._read_vacancies()
        return self.parser.parse_vacancies(vacancies_data)
    
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из JSON хранилища"""
        vacancies = self._read_vacancies()
        vacancies = [v for v in vacancies if v['alternate_url'] != vacancy.url]
        self._write_vacancies(vacancies) 