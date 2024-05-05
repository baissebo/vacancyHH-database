import requests
import json


def get_companies_vacancies():
    """
    Загружает имя компаний и их ID из файла companies_id.json,
    затем подключается к API HeadHunter и получает информацию о вакансиях для каждой компании
    :return: список словарей с информацией о вакансиях для каждой компании
    """
    with open('companies_id.json', 'r', encoding='utf-8') as f:
        companies_data = json.load(f)[0]

    vacancies_data = []
    for company_name, company_id in companies_data.items():
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)

        if response.status_code == 200:
            company_vacancies = {
                'company_name': company_name,
                'vacancies': response.json()['items']
            }
            vacancies_data.append(company_vacancies)
        else:
            print(f"Ошибка при запросе к API для компании {company_name}: {response.status_code}")

    return vacancies_data
