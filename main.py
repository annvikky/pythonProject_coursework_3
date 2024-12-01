from src.database import DBManager
from src.hh_api import HH
from src.utils import create_db, create_tables, fill_table_from_json, path, fill_table, del_data_from_table

db_manager = DBManager()


def user_interaction():
    """ Функция для взаимодействия с пользователем."""
    search_query = input("Введите запрос для поиска вакансии: ")
    print(f"Мы подбираем вакансии по вашему запросу: {search_query}... Пожалуйста, подождите!\n")

    create_db()
    create_tables()

    del_data_from_table("vacancies")
    del_data_from_table("employers")

    fill_table_from_json("employers", path)

    # получение вакансий по заданному фильтру через подключение к api
    hh_api = HH()
    hh_vacancies = hh_api.get_vacancies(search_query)
    # print(hh_vacancies)
    fill_table("vacancies", hh_vacancies)

    if hh_vacancies:
        # предложение выбора дальнейших действий с полученными данными
        print("Для максимального соответствия результатов поиска, пожалуйста, выберите действие: ")
        print("1. Показать список всех компаний и количество вакансий у каждой компании (Введите: 1)")
        print("2. Показать список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки "
              "на вакансию. (Введите: 2)")
        print("3. Показать среднюю зарплату по вакансиям (Ведите: 3)")
        print("4. Показать список всех вакансий, у которых зарплата выше средней по всем вакансиям (Введите: 4)")
        print("5. Показать список всех вакансий, в названии которых содержатся переданные в запросе слова (Введите: 5)")

    try:
        action = int(input("Введите цифру от 1 до 5: "))
    except ValueError:
        print("Ваш выбор не распознан. Выводим данные по действию 1")
        action = 1
    else:
        if action not in range(1, 6):
            print("Ваш выбор не распознан. Выводим данные по действию 1")
            action = 1

    if action == 1:
        db_manager.get_companies_and_vacancies_count()
    elif action == 2:
        db_manager.get_all_vacancies()
    elif action == 3:
        db_manager.get_avg_salary()
    elif action == 4:
        db_manager.get_vacancies_with_higher_salary()
    elif action == 5:
        db_manager.get_vacancies_with_keyword(search_query)


if __name__ == "__main__":
    user_interaction()
