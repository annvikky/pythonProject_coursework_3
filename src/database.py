import psycopg2


class DBManager:
    """Класс для подключения к БД PostgresSQL."""

    def __init__(self):
        self.conn = self.__connect_to_db()
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    @staticmethod
    def __connect_to_db():
        return psycopg2.connect(
            host="localhost",
            database="hh_database",
            user="postgres",
            password="123456",
            port="5432",
        )

    def get_companies_and_vacancies_count(self) -> None:
        """Метод получает список всех компаний и количество вакансий у каждой компании."""

        self.cur.execute(
            """
SELECT employers.employer_name, COUNT(vacancies.employer) 
FROM vacancies 
JOIN employers ON vacancies.employer = employers.employer_id 
GROUP BY employers.employer_name 
ORDER BY COUNT DESC
"""
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def get_all_vacancies(self) -> None:
        """Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
        на вакансию."""
        self.cur.execute(
            """
SELECT employers.employer_name, vacancy_name, salary, url FROM vacancies
JOIN employers ON vacancies.employer = employers.employer_id
ORDER BY employers.employer_name
            """
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def get_avg_salary(self) -> None:
        """Метод получает среднюю зарплату по вакансиям."""
        self.cur.execute(
            """
SELECT AVG(salary)
FROM vacancies
            """
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def get_vacancies_with_higher_salary(self) -> None:
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cur.execute(
            """
SELECT vacancy_name, salary, url FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)

    def get_vacancies_with_keyword(self, keyword: str) -> None:
        """Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        self.cur.execute(
            f"""
SELECT * FROM vacancies
WHERE vacancy_name LIKE '%{keyword}%'\
            """
        )
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
