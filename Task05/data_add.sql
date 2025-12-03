-- Добавление 5 новых пользователей
INSERT INTO users (first_name, last_name, email, gender_id)
VALUES 
    ("Елизавета", "Ямашкина", "yamashkina.elizaveta@example.com", 
        (SELECT id FROM genders WHERE code = "F")),
    
    ("Любовь", "Шаляева", "shalyaeva.lyubov@example.com",
        (SELECT id FROM genders WHERE code = "F")),
    
    ("Ксения", "Зельцер", "zeltser.ksenia@example.com",
        (SELECT id FROM genders WHERE code = "F")),
    
    ("Ян", "Моисеев", "moiseev.yan@example.com",
        (SELECT id FROM genders WHERE code = "M")),
    
    ("Екатерина", "Балакшина", "balakshina.ekaterina@example.com",
        (SELECT id FROM genders WHERE code = "F"));

-- Добавление 3 новых фильмов разных жанров
INSERT INTO movies (title, release_year, genre_id)
VALUES 
    ("Интерстеллар", 2014,
        (SELECT id FROM genres WHERE name = "Фантастика")),
    
    ("Невероятный мир глазами Энцо", 2019,
        (SELECT id FROM genres WHERE name = "Драма")),
    
    ("Аватар", 2009,
        (SELECT id FROM genres WHERE name = "Фантастика"));

-- Добавление 3 отзывов от вас (Елизавета Ямашкина)
INSERT INTO reviews (user_id, movie_id, rating, review_text)
VALUES 
    ((SELECT id FROM users WHERE email = "yamashkina.elizaveta@example.com"),
     (SELECT id FROM movies WHERE title = "Интерстеллар"),
     4.8, "Потрясающая научная фантастика с глубоким философским смыслом. Визуальные эффекты и музыка на высшем уровне."),
    
    ((SELECT id FROM users WHERE email = "yamashkina.elizaveta@example.com"),
     (SELECT id FROM movies WHERE title = "Невероятный мир глазами Энцо"),
     4.2, "Трогательная история о дружбе человека и собаки. Заставляет задуматься о важных жизненных ценностях."),
    
    ((SELECT id FROM users WHERE email = "yamashkina.elizaveta@example.com"),
     (SELECT id FROM movies WHERE title = "Аватар"),
     4.5, "Революционный фильм в плане визуальных эффектов. Захватывающий мир Пандоры и важный экологический посыл.");
