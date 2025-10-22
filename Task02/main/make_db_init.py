import os
import sqlite3


def escape_sql_value(value):
    """Экранирование специальных символов для SQL"""
    if value is None:
        return 'NULL'
    return str(value).replace("'", "''")


def detect_delimiter(line):
    """Автоопределение разделителя в строке"""
    delimiters = [',', ';', '|', '\t', '::']
    for delimiter in delimiters:
        if delimiter in line:
            return delimiter
    return ','  # разделитель по умолчанию


def generate_db_init():
    """Генерация SQL-скрипта для инициализации БД"""

    # Создаем SQL-скрипт
    with open('db_init.sql', 'w', encoding='utf-8') as f:
        # Удаляем существующие таблицы
        f.write('-- Удаление существующих таблиц\n')
        f.write('DROP TABLE IF EXISTS tags;\n')
        f.write('DROP TABLE IF EXISTS ratings;\n')
        f.write('DROP TABLE IF EXISTS movies;\n')
        f.write('DROP TABLE IF EXISTS users;\n\n')

        # Создаем таблицы
        f.write('-- Создание таблиц\n')
        f.write('''CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    genres TEXT
);\n\n''')

        f.write('''CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);\n\n''')

        f.write('''CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);\n\n''')

        f.write('''CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    gender TEXT,
    register_date TEXT,
    occupation TEXT
);\n\n''')

        # Загружаем данные из файлов dataset
        f.write('-- Загрузка данных в таблицу movies\n')
        movies_files = ['movies.csv', 'movies.dat', 'movies.txt']
        for movies_file in movies_files:
            if os.path.exists(f'dataset/{movies_file}'):
                with open(f'dataset/{movies_file}', 'r', encoding='utf-8') as file:
                    first_line = True
                    for line in file:
                        if first_line:
                            # Пропускаем заголовок если это CSV
                            if movies_file.endswith('.csv'):
                                first_line = False
                                continue
                            first_line = False

                        delimiter = detect_delimiter(line)
                        parts = line.strip().split(delimiter)
                        if len(parts) >= 3:
                            movie_id = parts[0]
                            title = escape_sql_value(parts[1])
                            genres = escape_sql_value(parts[2])
                            f.write(
                                f"INSERT INTO movies (id, title, genres) VALUES ({movie_id}, '{title}', '{genres}');\n")
                break  # Используем первый найденный файл

        f.write('\n-- Загрузка данных в таблицу ratings\n')
        ratings_files = ['ratings.csv', 'ratings.dat', 'ratings.txt']
        for ratings_file in ratings_files:
            if os.path.exists(f'dataset/{ratings_file}'):
                with open(f'dataset/{ratings_file}', 'r', encoding='utf-8') as file:
                    first_line = True
                    for line in file:
                        if first_line and ratings_file.endswith('.csv'):
                            first_line = False
                            continue

                        delimiter = detect_delimiter(line)
                        parts = line.strip().split(delimiter)
                        if len(parts) >= 4:
                            user_id = parts[0]
                            movie_id = parts[1]
                            rating = parts[2]
                            timestamp = parts[3]
                            f.write(
                                f"INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES ({user_id}, {movie_id}, {rating}, {timestamp});\n")
                break

        f.write('\n-- Загрузка данных в таблицу tags\n')
        tags_files = ['tags.csv', 'tags.dat', 'tags.txt']
        for tags_file in tags_files:
            if os.path.exists(f'dataset/{tags_file}'):
                with open(f'dataset/{tags_file}', 'r', encoding='utf-8') as file:
                    first_line = True
                    for line in file:
                        if first_line and tags_file.endswith('.csv'):
                            first_line = False
                            continue

                        delimiter = detect_delimiter(line)
                        parts = line.strip().split(delimiter)
                        if len(parts) >= 4:
                            user_id = parts[0]
                            movie_id = parts[1]
                            tag = escape_sql_value(parts[2])
                            timestamp = parts[3]
                            f.write(
                                f"INSERT INTO tags (user_id, movie_id, tag, timestamp) VALUES ({user_id}, {movie_id}, '{tag}', {timestamp});\n")
                break

        f.write('\n-- Загрузка данных в таблицу users\n')
        users_files = ['users.txt', 'users.csv', 'users.dat']
        for users_file in users_files:
            if os.path.exists(f'dataset/{users_file}'):
                with open(f'dataset/{users_file}', 'r', encoding='utf-8') as file:
                    first_line = True
                    for line in file:
                        if first_line and users_file.endswith('.csv'):
                            first_line = False
                            continue

                        delimiter = detect_delimiter(line)
                        parts = line.strip().split(delimiter)
                        if len(parts) >= 5:
                            user_id = parts[0]
                            name = escape_sql_value(parts[1])
                            email = escape_sql_value(parts[2])
                            gender = escape_sql_value(parts[3])
                            register_date = escape_sql_value(parts[4])
                            occupation = escape_sql_value(parts[5]) if len(parts) > 5 else 'NULL'
                            f.write(
                                f"INSERT INTO users (id, name, email, gender, register_date, occupation) VALUES ({user_id}, '{name}', '{email}', '{gender}', '{register_date}', '{occupation}');\n")
                break

        # УБРАНА КОМАНДА COMMIT - она не нужна
        # f.write('\n-- Коммит изменений\n')
        # f.write('COMMIT;\n')


if __name__ == "__main__":
    print("Генерация SQL-скрипта для инициализации БД...")
    generate_db_init()
    print("SQL-скрипт db_init.sql успешно создан!")