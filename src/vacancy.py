from dataclasses import dataclass
from typing import Optional

@dataclass
class Vacancy:
    """Класс для представления вакансии"""
    
    title: str
    url: str
    salary: Optional[dict]
    description: str
    requirements: str
    
    def __post_init__(self):
        """Проверка и обработка данных после инициализации"""
        if not self.title:
            raise ValueError("Название не может быть пустым")
        if not self.url:
            raise ValueError("URL не может быть пустым")
        if not self.description:
            self.description = "Описание не предоставлено"
        if not self.requirements:
            self.requirements = "Требования не указаны"
            
        # Обработка зарплаты
        if self.salary:
            self.salary_from = self.salary.get('from')
            self.salary_to = self.salary.get('to')
            self.salary_currency = self.salary.get('currency', 'RUR')
        else:
            self.salary_from = None
            self.salary_to = None
            self.salary_currency = 'RUR'
    
    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_str = f"{self.salary_from}-{self.salary_to} {self.salary_currency}" if self.salary_from is not None or self.salary_to is not None else "Зарплата не указана"
        return f"Вакансия: {self.title}\nURL: {self.url}\nЗарплата: {salary_str}\nОписание: {self.description}\nТребования: {self.requirements}"
    
    def __lt__(self, other) -> bool:
        """Сравнение "меньше" на основе зарплаты"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        
        # Если у одной из вакансий зарплата не указана, считаем её меньше
        if self.salary_from is None:
            return True
        if other.salary_from is None:
            return False
            
        return self.salary_from < other.salary_from
    
    def __gt__(self, other) -> bool:
        """Сравнение "больше" на основе зарплаты"""
        if not isinstance(other, Vacancy):
            return NotImplemented
            
        # Если у одной из вакансий зарплата не указана, считаем её меньше
        if self.salary_from is None:
            return False
        if other.salary_from is None:
            return True
            
        return self.salary_from > other.salary_from
    
    def __eq__(self, other) -> bool:
        """Сравнение на равенство на основе зарплаты"""
        if not isinstance(other, Vacancy):
            return NotImplemented
            
        # Если у одной из вакансий зарплата не указана, они не равны
        if self.salary_from is None or other.salary_from is None:
            return False
            
        return self.salary_from == other.salary_from
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Vacancy':
        """Создание экземпляра Vacancy из словаря"""
        return cls(
            title=data.get('name', ''),
            url=data.get('alternate_url', ''),
            salary=data.get('salary'),
            description=data.get('description', ''),
            requirements=data.get('snippet', {}).get('requirement', '')
        )
    
    @classmethod
    def cast_to_object_list(cls, vacancies_data: list) -> list['Vacancy']:
        """Преобразование списка словарей вакансий в список объектов Vacancy"""
        return [cls.from_dict(vacancy) for vacancy in vacancies_data] 