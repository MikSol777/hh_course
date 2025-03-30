from typing import List
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.storage import JSONStorage
from src.parser import HeadHunterParser

def filter_vacancies_by_keyword(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """Фильтрация вакансий по ключевому слову в описании или требованиях (регистронезависимый поиск)"""
    keyword = keyword.lower()
    return [
        v for v in vacancies
        if keyword in v.description.lower() or 
           keyword in v.requirements.lower() or 
           keyword in v.title.lower()
    ]

def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """Получение топ N вакансий по зарплате"""
    return sorted(vacancies, reverse=True)[:n]

def print_vacancies(vacancies: List[Vacancy]) -> bool:
    """Вывод вакансий в отформатированном виде. Возвращает True если вакансии найдены, False если нет."""
    if not vacancies:
        print("Вакансии не найдены")
        return False
    
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy}\n")
    return True

def user_interaction():
    """Основная функция взаимодействия с пользователем"""
    # Инициализация API, парсера и хранилища
    hh_api = HeadHunterAPI()
    hh_parser = HeadHunterParser()
    storage = JSONStorage()
    
    while True:
        print("\n=== Поиск вакансий на HeadHunter ===")
        print("1. Поиск вакансий")
        print("2. Показать сохраненные вакансии")
        print("3. Выход")
        
        choice = input("\nВыберите действие (1-3): ").strip()
        
        if choice == "1":
            search_query = input("Введите поисковый запрос: ").strip()
            print("\nПоиск вакансий...")
            
            # Получение вакансий из API и их парсинг
            vacancies_data = hh_api.get_vacancies(search_query)
            vacancies = hh_parser.parse_vacancies(vacancies_data)
            
            if not vacancies:
                print("Вакансии не найдены")
                continue
            
            # Сохранение вакансий в хранилище
            for vacancy in vacancies:
                storage.add_vacancy(vacancy)
            
            print(f"\nНайдено {len(vacancies)} вакансий")
            
            # Дополнительные опции фильтрации
            while True:
                print("\nДополнительные опции:")
                print("1. Показать топ N вакансий по зарплате")
                print("2. Фильтровать по ключевому слову")
                print("3. Вернуться в главное меню")
                
                filter_choice = input("\nВыберите действие (1-3): ").strip()
                
                if filter_choice == "1":
                    try:
                        n = int(input("Введите количество вакансий для вывода: ").strip())
                        top_vacancies = get_top_vacancies(vacancies, n)
                        if not print_vacancies(top_vacancies):
                            break
                    except ValueError:
                        print("Пожалуйста, введите корректное число")
                
                elif filter_choice == "2":
                    keyword = input("Введите ключевое слово для фильтрации: ").strip()
                    filtered_vacancies = filter_vacancies_by_keyword(vacancies, keyword)
                    if not print_vacancies(filtered_vacancies):
                        break
                
                elif filter_choice == "3":
                    break
                
                else:
                    print("Неверный выбор. Попробуйте снова.")
        
        elif choice == "2":
            print("\nСохраненные вакансии:")
            saved_vacancies = storage.get_vacancies()
            if not print_vacancies(saved_vacancies):
                continue
        
        elif choice == "3":
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    user_interaction()
