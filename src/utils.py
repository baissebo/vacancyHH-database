import json

import requests
import psycopg2


def get_companies():
    """
    Получает имя компаний и их ID из файла companies_id.json,
    :return: словарь с информацией о компаниях
    """
    with open('companies_id.json', 'r', encoding='utf-8') as f:
        companies_data = json.load(f)[0]

    companies_info = {}

    for company_name, company_id in companies_data.items():
        company_url = f"https://hh.ru/employer/{company_id}"
        companies_info[company_name] = {'company_id': company_id, 'company_url': company_url}

    return companies_info


def get_vacancies(companies_info):
    """
    Получает информацию о вакансиях для компаний из словаря companies_data
    :param companies_info: словарь с именами компаний и их id
    :return: словарь с информацией о вакансиях для каждой компании
    """
    vacancies_info = {}
    for company_name, company_data in companies_info.items():
        company_id = company_data['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()['items']
            vacancies_info[company_name] = vacancies
        else:
            print(f"Ошибка при запросе к API для компании {company_name}: {response.status_code}")
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
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
            vacancy_id integer PRIMARY KEY,
            company_id int REFERENCES companies(company_id),
            vacancy_name varchar(100) NOT NULL,
            requirement varchar(255),
            salary_min integer,
            salary_max integer,
            currency varchar(50),
            vacancy_url text
        """)

    conn.commit()
    conn.close()

