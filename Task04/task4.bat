#!/bin/bash
chcp 65001

sqlite3 movies_rating.db < db_init.sql

echo "1. Найти все пары пользователей, оценивших один и тот же фильм. Устранить дубликаты, проверить отсутствие пар с самим собой."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT DISTINCT 
    u1.name as user1, 
    u2.name as user2, 
    m.title as movie
FROM ratings r1
JOIN ratings r2 ON r1.movie_id = r2.movie_id AND r1.user_id < r2.user_id
JOIN users u1 ON r1.user_id = u1.id
JOIN users u2 ON r2.user_id = u2.id
JOIN movies m ON r1.movie_id = m.id
ORDER BY u1.name, u2.name, m.title
LIMIT 100;"
echo " "

echo "2. Найти 10 самых старых оценок от разных пользователей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT DISTINCT
    m.title,
    u.name,
    r.rating,
    date(datetime(r.timestamp, 'unixepoch')) as rating_date
FROM ratings r
JOIN users u ON r.user_id = u.id
JOIN movies m ON r.movie_id = m.id
ORDER BY r.timestamp ASC
LIMIT 10;"
echo " "

echo "3. Вывести фильмы с максимальным и минимальным средним рейтингом."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH MovieRatings AS (
    SELECT 
        m.title,
        m.year,
        AVG(r.rating) as avg_rating,
        CASE WHEN AVG(r.rating) = (SELECT MAX(avg_rating) FROM (SELECT AVG(rating) as avg_rating FROM ratings GROUP BY movie_id))
             THEN 'Да'
             WHEN AVG(r.rating) = (SELECT MIN(avg_rating) FROM (SELECT AVG(rating) as avg_rating FROM ratings WHERE rating IS NOT NULL GROUP BY movie_id))
             THEN 'Нет'
        END as recommend
    FROM movies m
    JOIN ratings r ON m.id = r.movie_id
    GROUP BY m.id, m.title, m.year
    HAVING avg_rating IS NOT NULL
)
SELECT title, year, avg_rating, recommend
FROM MovieRatings
WHERE recommend IS NOT NULL
ORDER BY year, title;"
echo " "

echo "4. Вычислить количество оценок и среднюю оценку от мужчин в период с 2011 по 2014 год."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT 
    COUNT(*) as ratings_count,
    ROUND(AVG(r.rating), 2) as avg_rating
FROM ratings r
JOIN users u ON r.user_id = u.id
WHERE u.gender = 'M'
AND strftime('%Y', datetime(r.timestamp, 'unixepoch')) BETWEEN '2011' AND '2014';"
echo " "

echo "5. Составить список фильмов с указанием средней оценки и количества пользователей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT 
    m.title,
    m.year,
    ROUND(AVG(r.rating), 2) as avg_rating,
    COUNT(DISTINCT r.user_id) as users_count
FROM movies m
JOIN ratings r ON m.id = r.movie_id
GROUP BY m.id, m.title, m.year
ORDER BY m.year, m.title
LIMIT 20;"
echo " "

echo "6. Определить самый распространенный жанр фильма."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH GenreCounts AS (
    SELECT 
        trim(value) as genre,
        COUNT(*) as movie_count
    FROM movies, json_each('[' || replace(genres, '|', ',') || ']')
    WHERE genres IS NOT NULL AND genres != ''
    GROUP BY genre
    ORDER BY movie_count DESC
)
SELECT genre, movie_count
FROM GenreCounts
LIMIT 1;"
echo " "

echo "7. Вывести список из 10 последних зарегистрированных пользователей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT 
    substr(name, instr(name, ' ') + 1) || ' ' || substr(name, 1, instr(name, ' ') - 1) as full_name,
    register_date
FROM users
WHERE name LIKE '% %'
ORDER BY register_date DESC
LIMIT 10;"
echo " "

echo "8. Определить, на какие дни недели приходился ваш день рождения в каждом году."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "WITH RECURSIVE years(year) AS (
    SELECT 2000
    UNION ALL
    SELECT year + 1 FROM years WHERE year < 2023
)
SELECT 
    year,
    strftime('%Y-%m-%d', year || '-08-15') as birthday,
    CASE strftime('%w', year || '-08-15')
        WHEN '0' THEN 'Воскресенье'
        WHEN '1' THEN 'Понедельник'
        WHEN '2' THEN 'Вторник'
        WHEN '3' THEN 'Среда'
        WHEN '4' THEN 'Четверг'
        WHEN '5' THEN 'Пятница'
        WHEN '6' THEN 'Суббота'
    END as day_of_week
FROM years
ORDER BY year;"
echo " "
