from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any

class JobAPI(ABC):
    """Абстрактный базовый класс для API вакансий"""
    
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получение вакансий из API"""
        pass

class HeadHunterAPI(JobAPI):
    """Реализация API HeadHunter"""
    
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получение вакансий из API HeadHunter"""
        params = {
            "text": search_query,
            "area": 1,  # 1 - код для России
            "per_page": 100
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()["items"]
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Ошибка при получении вакансий: {e}")
            return [] 