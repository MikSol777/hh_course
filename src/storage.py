from abc import ABC, abstractmethod
import json
from typing import List, Optional
from .vacancy import Vacancy
from .parser import HeadHunterParser
from .utils import load_vacancies, save_vacancies, vacancy_to_dict, dict_to_vacancy

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
    """Класс для работы с JSON-файлом"""
    
    def __init__(self, file_path: str = "vacancies.json"):
        """
        Инициализация хранилища
        
        Args:
            file_path (str): Путь к файлу для хранения вакансий. По умолчанию "vacancies.json"
        """
        self.__file_path = file_path
        self.__vacancies = load_vacancies(file_path)
    
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавление вакансии в файл
        
        Args:
            vacancy (Vacancy): Вакансия для добавления
        """
        vacancy_dict = vacancy_to_dict(vacancy)
        # Проверяем, нет ли уже такой вакансии
        if not any(v.get('alternate_url') == vacancy_dict['alternate_url'] for v in self.__vacancies):
            self.__vacancies.append(vacancy_dict)
            save_vacancies(self.__file_path, self.__vacancies)
    
    def get_vacancies(self) -> List[Vacancy]:
        """
        Получение вакансий из файла
        
        Returns:
            List[Vacancy]: Список вакансий
        """
        return [dict_to_vacancy(v) for v in self.__vacancies]
    
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаление вакансии из файла
        
        Args:
            vacancy (Vacancy): Вакансия для удаления
        """
        self.__vacancies = [v for v in self.__vacancies if v.get('alternate_url') != vacancy.url]
        save_vacancies(self.__file_path, self.__vacancies) 