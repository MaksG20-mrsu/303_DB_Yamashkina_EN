from database import create_connection, execute_query

def init_database():
    conn = create_connection()
    
    # Создание таблиц
    create_groups_table = """
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_number TEXT NOT NULL UNIQUE,
        specialization TEXT NOT NULL,
        year_started INTEGER NOT NULL,
        current_year INTEGER DEFAULT 1
    );
    """
    
    create_students_table = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT,
        group_id INTEGER NOT NULL,
        gender TEXT CHECK(gender IN ('М', 'Ж')),
        birth_date DATE,
        FOREIGN KEY (group_id) REFERENCES groups (id)
    );
    """
    
    create_disciplines_table = """
    CREATE TABLE IF NOT EXISTS disciplines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        year_of_study INTEGER NOT NULL,
        semester INTEGER CHECK(semester IN (1, 2))
    );
    """
    
    create_exams_table = """
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        discipline_id INTEGER NOT NULL,
        exam_date DATE NOT NULL,
        grade INTEGER CHECK(grade >= 2 AND grade <= 5),
        semester INTEGER CHECK(semester IN (1, 2)),
        year_of_study INTEGER CHECK(year_of_study >= 1 AND year_of_study <= 6),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (discipline_id) REFERENCES disciplines (id)
    );
    """
    
    execute_query(conn, create_groups_table)
    execute_query(conn, create_students_table)
    execute_query(conn, create_disciplines_table)
    execute_query(conn, create_exams_table)
    
    # Заполнение справочников начальными данными
    insert_groups = """
    INSERT OR IGNORE INTO groups (group_number, specialization, year_started, current_year) VALUES
    ('ИВТ-101', 'Информатика и вычислительная техника', 2023, 1),
    ('ИВТ-102', 'Информатика и вычислительная техника', 2023, 1),
    ('ПИ-201', 'Прикладная информатика', 2022, 2),
    ('ПИ-202', 'Прикладная информатика', 2022, 2),
    ('ИБ-301', 'Информационная безопасность', 2021, 3);
    """
    
    insert_disciplines = """
    INSERT OR IGNORE INTO disciplines (name, specialization, year_of_study, semester) VALUES
    ('Математический анализ', 'Информатика и вычислительная техника', 1, 1),
    ('Программирование', 'Информатика и вычислительная техника', 1, 1),
    ('Физика', 'Информатика и вычислительная техника', 1, 2),
    ('Базы данных', 'Информатика и вычислительная техника', 2, 1),
    ('Операционные системы', 'Информатика и вычислительная техника', 2, 2),
    ('Прикладная математика', 'Прикладная информатика', 2, 1),
    ('Веб-технологии', 'Прикладная информатика', 2, 2),
    ('Криптография', 'Информационная безопасность', 3, 1),
    ('Сетевые технологии', 'Информационная безопасность', 3, 2);
    """
    
    execute_query(conn, insert_groups)
    execute_query(conn, insert_disciplines)
    
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()