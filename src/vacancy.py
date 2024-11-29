class Vacancy:
    """Класс для работы с вакансиями."""

    __slots__ = (
        "name",
        "url",
        "salary",
        "requirement",
        "responsibility",
        "area",
        "employer_id",
        "employer",
    )

    def __init__(
        self,
        name: str,
        url: str,
        requirement: str,
        responsibility: str,
        area: str,
        employer_id: int,
        employer: str,
        salary: int = 0,
    ):
        self.name = name
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility
        self.salary = self.__salary_is_valid(salary)
        self.area = area
        self.employer_id = employer_id
        self.employer = employer

    @staticmethod
    def __salary_is_valid(salary: int) -> int:
        """Метод для валидации зарплаты."""
        if salary:
            return int(salary)
        else:
            return 0

    @classmethod
    def cast_to_object_list(cls, vacancies: list[dict]) -> list["Vacancy"]:
        """Возвращает список экземпляров класса из списка словарей."""
        return [cls(**vacancy) for vacancy in vacancies]

    def get_to_dict(self) -> dict[str, str | int]:
        """Возвращает словарь с описанием вакансии из экземпляра класса."""
        return {
            "name": self.name,
            "url": self.url,
            "requirement": self.requirement,
            "responsibility": self.responsibility,
            "salary": self.salary,
            "area": self.area,
            "employer_id": self.employer_id,
            "employer": self.employer,
        }

    def __eq__(self, other) -> bool:
        """Магический метод сравнения вакансий по зарплате (=)."""
        if not isinstance(other, (int, Vacancy)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")

        salary_for_comparison = other if isinstance(other, int) else other.salary
        return self.salary == salary_for_comparison

    def __lt__(self, other) -> bool:
        """Магический метод сравнения вакансий по зарплате (<)."""
        if not isinstance(other, (int, Vacancy)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")

        salary_for_comparison = other if isinstance(other, int) else other.salary
        return self.salary < salary_for_comparison

    def __gt__(self, other) -> bool:
        """Магический метод сравнения вакансий по зарплате (>)."""
        if not isinstance(other, (int, Vacancy)):
            raise TypeError("Операнд справа должен иметь тип int или Vacancy")

        salary_for_comparison = other if isinstance(other, int) else other.salary
        return self.salary > salary_for_comparison

    def __str__(self) -> str:
        """Метод строкового представления вакансий."""

        return f"""{self.name} (Зарплата: {self.salary if self.salary else 'не указана'}).
Требования: {self.requirement}.
Обязанности: {self.responsibility}.
Ссылка на вакансию: {self.url}.
Город: {self.area}.
Работодатель: {self.employer_id}, {self.employer}.
"""
