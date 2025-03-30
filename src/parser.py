from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .vacancy import Vacancy

class Parser(ABC):
    """Абстрактный базовый класс для парсера данных вакансий"""
    
    @abstractmethod
    def parse_vacancies(self, data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Парсинг данных вакансий в объекты Vacancy"""
        pass

class HeadHunterParser(Parser):
    """Реализация парсера для данных API HeadHunter"""
    
    def parse_vacancies(self, data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Парсинг данных вакансий HeadHunter в объекты Vacancy"""
        return Vacancy.cast_to_object_list(data) 