import json
from typing import Any

import requests
import psycopg2


def get_companies():
    """
    Получает имя компаний и их ID из файла companies_id.json,
    :return: список словарей с информацией о компаниях
    """
    with open('companies_id.json', 'r', encoding='utf-8') as f:
        companies_data = json.load(f)[0]

    data = []

    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
        data.append(company_info)

    return data


def get_vacancies(data):
    """
    Получает информацию о вакансиях для компаний из списка data
    :param data: список словарей с информацией о компаниях
    :return: список словарей с информацией о вакансиях для каждой компании
    """
    vacancies_info = []
    for company_data in data:
        company_id = company_data['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()['items']
            vacancies_info.extend(vacancies)
        else:
            print(f"Ошибка при запросе к API для компании {company_data['company_name']}: {response.status_code}")
    return vacancies_info


def create_db(database_name: str, params: dict) -> None:
    """
    Создание базы данных для сохранения данных о компаниях и вакансиях
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")
    except Exception as e:
        print(f"Ошибка создания базы данных: {e}")
    finally:
        cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
            company_id integer PRIMARY KEY,
            company_name varchar(50) NOT NULL,
            company_url text
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
            vacancy_id text PRIMARY KEY,
            company_id integer REFERENCES companies(company_id),
            vacancy_name varchar(100) NOT NULL,
            requirement varchar(255),
            salary_min integer,
            salary_max integer,
            currency varchar(50),
            vacancy_url text
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_db(companies_data: list[dict[str, Any]],
                    vacancies_data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных."""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in companies_data:
            company_id = company['company_id']
            company_name = company['company_name']
            company_url = company['company_url']
            cur.execute("""
                INSERT INTO companies (company_id, company_name, company_url)
                VALUES (%s, %s, %s)
            """, (company_id, company_name, company_url))

        for vacancy in vacancies_data:
            vacancy_id = vacancy['id']
            company_id = vacancy['employer']['id']
            vacancy_name = vacancy['name']
            requirement = vacancy['snippet'].get('requirement', None)
            salary = vacancy['salary']
            salary_min = salary.get('from') if salary else None
            salary_max = salary.get('to') if salary else None
            currency = salary.get('currency', None) if salary else None
            vacancy_url = vacancy['alternate_url']
            cur.execute("""
                INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, requirement, salary_min, salary_max,
                currency, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (vacancy_id, company_id, vacancy_name, requirement, salary_min, salary_max, currency, vacancy_url))

    conn.commit()
    conn.close()
