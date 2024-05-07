import os
from config import config
from utils import get_companies, get_vacancies, create_db, save_data_to_db


def main():
    companies_data = get_companies()
    vacancies_data = get_vacancies(companies_data)
    params = config()

    create_db('vacancies_hh', params)
    save_data_to_db(companies_data, vacancies_data, 'vacancies_hh', params)


if __name__ == '__main__':
    main()
