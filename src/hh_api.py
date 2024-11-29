from abc import ABC, abstractmethod

import requests
from requests import Response


class Parser(ABC):
    """Класс для работы API сервиса с вакансиями"""

    @abstractmethod
    def connect_to_api(self) -> Response:
        pass

    @abstractmethod
    def get_vacancies(self, keyword) -> list:
        pass


class HH(Parser):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        """Инициализация класса."""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def __connect_to_api(self) -> Response | int:
        """Подключение к API hh.ru."""
        response = requests.get(
            self.__url, headers=self.__headers, params=self.__params
        )
        if response.status_code == 200:
            return response
        else:
            return response.status_code
            # print("Ошибка подключения к ресурсу hh.ru")

    @property
    def connect_to_api(self) -> Response:
        """Геттер для подключения к api."""
        return self.__connect_to_api()

    def get_vacancies(self, keyword: str) -> list:
        """Получения списка вакансий по заданному фильтру в json."""
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = self.__connect_to_api()
            if response:
                response_json = response.json()
                vacancies = response_json["items"]
                self.__vacancies.extend(vacancies)

                pages = response_json.get("pages")
                if not pages or pages <= self.__params.get("page"):
                    break

                self.__params["page"] += 1

            else:
                break

        vacancies_list = []
        if self.__vacancies:

            # получение списка словарей с ключами name, url, requirement, responsibility, salary, area, employer_id,
            # employer
            for vacancy in self.__vacancies:
                name = vacancy.get("name")
                url = vacancy.get("alternate_url")
                requirement = vacancy.get("snippet").get("requirement")
                responsibility = vacancy.get("snippet").get("responsibility")
                salary = vacancy.get("salary")
                area = vacancy.get("area").get("name")
                employer_id = vacancy.get("employer").get("id")
                employer = vacancy.get("employer").get("name")

                if salary:
                    salary = salary.get("from")

                vacancy = {
                    "name": name,
                    "url": url,
                    "requirement": requirement,
                    "responsibility": responsibility,
                    "salary": salary,
                    "area": area,
                    "employer_id": employer_id,
                    "employer": employer,
                }
                vacancies_list.append(vacancy)

        return vacancies_list
