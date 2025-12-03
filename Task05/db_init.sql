-- Создание таблицы полов (справочник)
CREATE TABLE IF NOT EXISTS genders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(20) NOT NULL UNIQUE
);

-- Создание таблицы жанров (справочник)
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    gender_id INTEGER NOT NULL DEFAULT 1,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (gender_id) REFERENCES genders(id) ON DELETE RESTRICT,
    CHECK (email LIKE '%@%')
);

-- Создание таблицы фильмов
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    release_year INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE RESTRICT,
    CHECK (release_year BETWEEN 1888 AND 2100)
);

-- Создание таблицы отзывов
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL DEFAULT 0,
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE RESTRICT,
    CHECK (rating >= 0 AND rating <= 5)
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_users_last_name ON users(last_name);
CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);
CREATE INDEX IF NOT EXISTS idx_movies_year ON movies(release_year);
CREATE INDEX IF NOT EXISTS idx_reviews_user_movie ON reviews(user_id, movie_id);

-- Заполнение справочника полов
INSERT OR IGNORE INTO genders (code, name) VALUES
    ("M", "Мужской"),
    ("F", "Женский");

-- Заполнение справочника жанров
INSERT OR IGNORE INTO genres (name) VALUES
    ("Драма"),
    ("Комедия"),
    ("Боевик"),
    ("Фантастика"),
    ("Триллер"),
    ("Ужасы"),
    ("Мелодрама"),
    ("Детектив"),
    ("Приключения"),
    ("Анимация");
