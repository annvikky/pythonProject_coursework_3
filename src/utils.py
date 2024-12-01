import json
import os
from typing import Any

import psycopg2

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json")


def create_db() -> None:
    """Создание БД в PostgresSQL."""
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="123456",
        port="5432",
    )

    # Открытие курсора
    cur = conn.cursor()
    conn.autocommit = True

    # cur.execute("DROP DATABASE IF EXISTS hh_database;")
    # cur.execute("CREATE DATABASE hh_database ENCODING 'UTF-8';")
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'hh_database'")
    exists = cur.fetchone()
    if not exists:
        cur.execute("CREATE DATABASE hh_database ENCODING 'UTF-8'")
    cur.close()
    conn.close()


def create_tables() -> None:
    """Создание таблиц в БД."""
    conn = psycopg2.connect(
        host="localhost",
        database="hh_database",
        user="postgres",
        password="123456",
        port="5432",
    )

    # Открытие курсора
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(
        """CREATE TABLE IF NOT EXISTS employers(
employer_id INT PRIMARY KEY,     
employer_name VARCHAR(25) NOT NULL   
    );
    """
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS vacancies(
        vacancy_id SERIAL PRIMARY KEY,
        vacancy_name VARCHAR(250) NOT NULL,
        requirement VARCHAR(500),
        responsibility VARCHAR(500),
        area VARCHAR(50) NOT NULL,
        employer INT NOT NULL,
        url VARCHAR(100) NOT NULL,
        salary INT,
FOREIGN KEY (employer) REFERENCES employers(employer_id) 
        );
        """
    )

    cur.close()
    conn.close()


def fill_table_from_json(table_name: str, data: Any) -> None:
    """Заполнение таблиц в БД."""
    conn = psycopg2.connect(
        host="localhost",
        database="hh_database",
        user="postgres",
        password="123456",
        port="5432",
    )

    # Открытие курсора
    cur = conn.cursor()
    conn.autocommit = True

    with open(data, "r", encoding="utf-8") as file:
        employers = json.load(file)
        for employer in employers.get("employers"):
            cur.execute(
                f"""
                INSERT INTO {table_name} (employer_id, employer_name) VALUES (%s, %s) """,
                (employer.get("id"), employer.get("employer_name")),
            )

    cur.close()
    conn.close()


def fill_table(table_name: str, vacancies_list: list) -> None:
    """Заполнение таблиц в БД."""
    conn = psycopg2.connect(
        host="localhost",
        database="hh_database",
        user="postgres",
        password="123456",
        port="5432",
    )

    # Открытие курсора
    cur = conn.cursor()
    conn.autocommit = True

    with open(path, "r", encoding="utf-8") as file:
        employers = json.load(file)
        employers_list = employers["employers"]
        emp_id = []

        for emp in employers_list:
            emp_id.append(emp.get("id"))

        for emp in emp_id:
            filtered_vacancies_list = [
                vac for vac in vacancies_list if vac.get("employer_id") == str(emp)
            ]

            for vacancy in filtered_vacancies_list:
                cur.execute(
                    f"""
INSERT INTO {table_name} (url, vacancy_name, requirement, responsibility, area, 
employer, salary) VALUES (%s, %s, %s, %s, %s, %s, %s) """,
                    (
                        vacancy.get("url"),
                        vacancy.get("name"),
                        vacancy.get("requirement"),
                        vacancy.get("responsibility"),
                        vacancy.get("area"),
                        vacancy.get("employer_id"),
                        vacancy.get("salary"),
                    ),
                )

    cur.close()
    conn.close()


def del_data_from_table(table_name: str) -> None:
    """Удаление данных из таблиц в БД."""
    conn = psycopg2.connect(
        host="localhost",
        database="hh_database",
        user="postgres",
        password="123456",
        port="5432",
    )

    # Открытие курсора
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f"DELETE FROM {table_name}")

    cur.close()
    conn.close()
