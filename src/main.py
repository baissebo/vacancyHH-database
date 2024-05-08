from config import config
from utils import get_companies, get_vacancies, create_db, save_data_to_db
from db_manager import DBManager


def main():
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    params = config()

    create_db('vacancies_hh', params)
    save_data_to_db(companies_data, vacancies_data, 'vacancies_hh', params)

    db_m = DBManager()

    print("""Введите ваш запрос:
          1 - Список всех компаний и количество вакансий у каждой компании
          2 - Cписок всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию          
          3 - Средняя зарплата по вакансиям
          4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям
          5 - Список всех вакансий, в названии которых содержатся ключевые слова""")

    user_input = input()
    if user_input == '1':
        companies_and_vacancies_count = db_m.get_companies_and_vacancies_count()
        print("Компании и количество доступных вакансий:")
        for company_name, vacancy_count in companies_and_vacancies_count:
            print(f"{company_name}: {vacancy_count}")
    elif user_input == '2':
        all_vacancies = db_m.get_all_vacancies()
        print("Все вакансии:")
        for vacancy in all_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max}, "
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '3':
        avg_salary = db_m.get_avg_salary()
        print(f"Средняя зарплата по всем вакансиям: {avg_salary}")
    elif user_input == '4':
        higher_salary_vacancies = db_m.get_vacancies_with_higher_salary()
        print("Вакансии с зарплатой выше средней:")
        for vacancy in higher_salary_vacancies:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    elif user_input == '5':
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        vacancies_with_keyword = db_m.get_vacancies_with_keyword(keyword)
        print(f"Все вакансии с ключевым словом '{keyword}':")
        for vacancy in vacancies_with_keyword:
            company_name, vacancy_name, salary_min, salary_max, vacancy_url = vacancy
            print(f"Компания: {company_name}, Вакансия: {vacancy_name}, Зарплата: {salary_min}-{salary_max},"
                  f"Ссылка на вакансию: {vacancy_url}")
    else:
        print("Некорректный ввод")


if __name__ == '__main__':
    main()
