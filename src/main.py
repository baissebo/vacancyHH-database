import os
from config import config
from utils import get_companies, get_vacancies,create_db


def main():
    companies_info = get_companies()
    vacancies_info = get_vacancies(companies_info)
    params = config()

    create_db('vacancies_hh', params)


if __name__ == '__main__':
    main()
