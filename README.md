# Python project: Поиск вакансий. Интеграция с внешним сервисом (hh.ru). 
# Проектирование таблиц БД PostgresSQL и загрузка полученных данных.

## Проект представляет собой приложение, позволяющее пользователю получать вакансии с внешнего сервиса.
## Полученные вакансии записываются в созданные таблицы БД PostgresSQL.
## Вакансии загружены по фильтру компаний, предусмотрен вывод вакансий по зарплате, компании, совпадению с ключевым словом.
## Осуществлена сборка приложения по функции main().

## Установка:
1. Клонируйте репозиторий по SHH-ключу:
    ```
    git@github.com:annvikky/pythonProject_coursework_3.git
    ```
2. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
## Использование: 

Для начала работы пользователю необходимо ввести поисковое слово, по которому будут отобраны вакансии.  
Создается база данных и таблицы, если они не созданы ранее.
Таблицы заполняются работодателями по заданному перечню и вакансиями от отобранных работодателей. 
По факту получения вакансий пользователю предлагаются действия с этими вакансиями.
Возможна фильтрация по имени вакансии.
Предусмотрена фильтрация по заработной плате выше среднего.
Возможен вывод количества вакансий по работодателям.

## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).

## Тестирование:

Данный раздел находится в разработке.