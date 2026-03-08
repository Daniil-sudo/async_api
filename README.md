# Star Wars Async Loader

Асинхронная загрузка персонажей из API **SWAPI** в базу данных **SQLite**.

Проект демонстрирует использование асинхронных запросов для получения данных из API и их сохранения в базу данных.

## Используемые технологии

* Python 3
* asyncio
* aiohttp
* aiosqlite
* SQLite

## Структура проекта

```
Async_api/
│
├── migration.sql        # скрипт создания таблицы
├── run_migration.py     # скрипт принудительного создания таблицы
├── load_characters.py   # асинхронная загрузка данных из API
├── check_db.py          # проверка содержимого базы
├── requirements.txt     # зависимости проекта
└── starwars.db          # база данных (создаётся автоматически)
```

## Установка зависимостей

Создать виртуальное окружение и установить библиотеки:

```
pip install -r requirements.txt
```

## Создание базы данных

В Windows PowerShell используйте команду:

```
sqlite3 starwars.db ".read migration.sql"
```

Если используется обычная командная строка (cmd):

```
sqlite3 starwars.db < migration.sql
```

## Загрузка персонажей

Запуск скрипта загрузки данных из API:

```
python load_characters.py
```

Скрипт:

* асинхронно получает персонажей из SWAPI
* получает информацию о родной планете
* сохраняет данные в таблицу `characters`

## Проверка данных

Чтобы посмотреть содержимое базы данных:

```
python check_db.py
```

## Загружаемые поля

В базу сохраняются следующие данные:

* id
* birth_year
* eye_color
* gender
* hair_color
* homeworld
* mass
* name
* skin_color

## Источник данных

API: https://www.swapi.tech/
