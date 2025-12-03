
CREATE TABLE masters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    hire_date DATE NOT NULL DEFAULT (date('now')),
    dismissal_date DATE,
    salary_percent REAL NOT NULL CHECK(salary_percent > 0 AND salary_percent <= 100),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1))
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    duration_minutes INTEGER NOT NULL CHECK(duration_minutes > 0),
    price REAL NOT NULL CHECK(price >= 0)
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL REFERENCES masters(id),
    appointment_datetime DATETIME NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
    created_at DATETIME NOT NULL DEFAULT (datetime('now')),
    client_name TEXT,
    client_phone TEXT
);

CREATE TABLE appointment_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id),
    UNIQUE(appointment_id, service_id)
);

CREATE TABLE completed_works (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id),
    master_id INTEGER NOT NULL REFERENCES masters(id),
    service_id INTEGER NOT NULL REFERENCES services(id),
    completed_datetime DATETIME NOT NULL DEFAULT (datetime('now')),
    actual_price REAL CHECK(actual_price >= 0)
);

CREATE TABLE master_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_id INTEGER NOT NULL REFERENCES masters(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK(day_of_week BETWEEN 0 AND 6), -- 0 = воскресенье, 1 = понедельник, ...
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CHECK(end_time > start_time)
);

CREATE INDEX idx_appointments_master_id ON appointments(master_id);
CREATE INDEX idx_appointments_datetime ON appointments(appointment_datetime);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_completed_works_master_id ON completed_works(master_id);
CREATE INDEX idx_completed_works_datetime ON completed_works(completed_datetime);
CREATE INDEX idx_appointment_services_appointment_id ON appointment_services(appointment_id);
CREATE INDEX idx_appointment_services_service_id ON appointment_services(service_id);


INSERT INTO masters (first_name, last_name, middle_name, hire_date, dismissal_date, salary_percent, is_active) VALUES
('Иван', 'Петров', 'Сергеевич', '2023-01-15', NULL, 25.5, 1),
('Мария', 'Сидорова', 'Александровна', '2022-06-10', NULL, 30.0, 1),
('Алексей', 'Козлов', 'Владимирович', '2023-03-20', '2024-01-10', 28.0, 0),
('Елена', 'Новикова', 'Игоревна', '2022-11-05', NULL, 27.5, 1),
('Дмитрий', 'Морозов', 'Андреевич', '2024-02-01', NULL, 26.0, 1);

INSERT INTO services (name, duration_minutes, price) VALUES
('Диагностика двигателя', 60, 1500.00),
('Замена масла', 30, 800.00),
('Замена тормозных колодок', 90, 2500.00),
('Регулировка развала-схождения', 45, 1200.00),
('Замена свечей зажигания', 40, 1000.00),
('Диагностика подвески', 50, 1300.00),
('Замена фильтров (воздушный, салонный)', 35, 900.00),
('Промывка системы охлаждения', 60, 1800.00),
('Ремонт кондиционера', 120, 3500.00),
('Шиномонтаж (4 колеса)', 60, 2000.00);

INSERT INTO master_schedule (master_id, day_of_week, start_time, end_time) VALUES
(1, 1, '09:00', '18:00'), -- Понедельник
(1, 2, '09:00', '18:00'), 
(1, 3, '09:00', '18:00'), 
(1, 4, '09:00', '18:00'), 
(1, 5, '09:00', '18:00'), 
(2, 1, '10:00', '19:00'),
(2, 2, '10:00', '19:00'),
(2, 3, '10:00', '19:00'),
(2, 4, '10:00', '19:00'),
(2, 5, '10:00', '19:00'),
(4, 1, '08:00', '17:00'),
(4, 2, '08:00', '17:00'),
(4, 3, '08:00', '17:00'),
(4, 4, '08:00', '17:00'),
(4, 5, '08:00', '17:00'),
(5, 2, '11:00', '20:00'),
(5, 3, '11:00', '20:00'),
(5, 4, '11:00', '20:00'),
(5, 5, '11:00', '20:00'),
(5, 6, '11:00', '20:00'); 

INSERT INTO appointments (master_id, appointment_datetime, status, created_at, client_name, client_phone) VALUES
(1, '2024-12-15 10:00:00', 'completed', '2024-12-10 14:30:00', 'Сергей Иванов', '+7-900-123-45-67'),
(1, '2024-12-15 14:00:00', 'completed', '2024-12-11 09:15:00', 'Анна Петрова', '+7-900-234-56-78'),
(2, '2024-12-16 11:00:00', 'completed', '2024-12-12 10:20:00', 'Владимир Сидоров', '+7-900-345-67-89'),
(4, '2024-12-17 09:00:00', 'completed', '2024-12-13 15:45:00', 'Ольга Козлова', '+7-900-456-78-90'),
(1, '2024-12-18 10:00:00', 'scheduled', '2024-12-14 11:00:00', 'Дмитрий Морозов', '+7-900-567-89-01'),
(2, '2024-12-18 15:00:00', 'scheduled', '2024-12-14 12:30:00', 'Елена Новикова', '+7-900-678-90-12'),
(5, '2024-12-19 12:00:00', 'scheduled', '2024-12-14 13:15:00', 'Игорь Волков', '+7-900-789-01-23'),
(4, '2024-12-20 10:00:00', 'scheduled', '2024-12-14 14:00:00', 'Татьяна Лебедева', '+7-900-890-12-34');


INSERT INTO appointment_services (appointment_id, service_id) VALUES
(1, 1),
(1, 2), 
(2, 3),
(3, 4),
(3, 5), 
(4, 6), 
(4, 7), 
(5, 1), 
(5, 2), 
(6, 8), 
(7, 9),
(8, 10);


INSERT INTO completed_works (appointment_id, master_id, service_id, completed_datetime, actual_price) VALUES
(1, 1, 1, '2024-12-15 10:45:00', 1500.00),
(1, 1, 2, '2024-12-15 11:15:00', 800.00),
(2, 1, 3, '2024-12-15 14:30:00', 2500.00),
(3, 2, 4, '2024-12-16 11:30:00', 1200.00),
(3, 2, 5, '2024-12-16 12:10:00', 1000.00),
(4, 4, 6, '2024-12-17 09:40:00', 1300.00),
(4, 4, 7, '2024-12-17 10:15:00', 900.00);