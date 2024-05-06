import os
from config import config
from utils import get_companies, get_vacancies, create_db


def main():
    data = get_companies()
    get_vacancies(data)
    params = config()

    create_db('vacancies_hh', params)
    # save_data_to_db(data, 'vacancies_hh', params)


if __name__ == '__main__':
    main()
