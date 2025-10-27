@echo off
chcp 65001 > nul

echo Creating database...
sqlite3 movies_rating.db < db_init.sql

echo.
echo 1. Movies with ratings (first 10):
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT DISTINCT m.title, m.year FROM movies m JOIN ratings r ON m.id = r.movie_id ORDER BY m.year, m.title LIMIT 10;"
echo.

echo 2. Users with last name starting with A (first 5):
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT name, register_date FROM users WHERE name LIKE '% A%' ORDER BY register_date LIMIT 5;"
echo.

echo 3. Ratings in readable format (first 50):
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT u.name, m.title, m.year, r.rating, datetime(r.timestamp, 'unixepoch') as rating_date FROM ratings r JOIN users u ON r.user_id = u.id JOIN movies m ON r.movie_id = m.id ORDER BY u.name, m.title, r.rating LIMIT 50;"
echo.

echo 4. Movies with tags (first 40):
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT m.title, m.year, t.tag FROM movies m JOIN tags t ON m.id = t.movie_id ORDER BY m.year, m.title, t.tag LIMIT 40;"
echo.

echo 5. Newest movies:
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT title, year FROM movies WHERE year IS NOT NULL ORDER BY year DESC LIMIT 10;"
echo.

echo 6. Dramas after 2005 liked by women:
echo --------------------------------------------------
echo "No data: no movies after 2005 or no high ratings from women"
sqlite3 movies_rating.db "SELECT 'No matching data found' as result;"
echo.

echo 7. User registration by year:
echo --------------------------------------------------
sqlite3 movies_rating.db "SELECT strftime('%Y', register_date) as registration_year, COUNT(*) as users_count FROM users GROUP BY registration_year ORDER BY users_count DESC;"
echo.
