from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import create_connection, execute_query, execute_read_query
from models import Student, Exam
from datetime import datetime

app = Flask(__name__)

# Главная страница - список студентов
@app.route('/')
def index():
    conn = create_connection()
    group_filter = request.args.get('group_filter', '')
    
    query = """
    SELECT s.*, g.group_number 
    FROM students s 
    JOIN groups g ON s.group_id = g.id
    """
    
    params = []
    if group_filter:
        query += " WHERE g.group_number = ?"
        params.append(group_filter)
    
    query += " ORDER BY g.group_number, s.last_name, s.first_name"
    
    students = execute_read_query(conn, query, params)
    
    # Получение списка групп для фильтра
    groups = execute_read_query(conn, "SELECT * FROM groups ORDER BY group_number")
    
    conn.close()
    
    return render_template('index.html', 
                         students=students, 
                         groups=groups, 
                         group_filter=group_filter)

# Добавление нового студента
@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = Student.from_dict(request.form)
        
        conn = create_connection()
        query = """
        INSERT INTO students (last_name, first_name, patronymic, group_id, gender, birth_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        student_id = execute_query(conn, query, (
            student.last_name,
            student.first_name,
            student.patronymic,
            student.group_id,
            student.gender,
            student.birth_date
        ))
        
        conn.close()
        return redirect(url_for('index'))
    
    conn = create_connection()
    groups = execute_read_query(conn, "SELECT * FROM groups ORDER BY group_number")
    conn.close()
    
    return render_template('student_form.html', 
                         student=None, 
                         groups=groups, 
                         action=url_for('add_student'))

# Редактирование студента
@app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    conn = create_connection()
    
    if request.method == 'POST':
        student = Student.from_dict(request.form)
        student.id = student_id
        
        query = """
        UPDATE students 
        SET last_name = ?, first_name = ?, patronymic = ?, 
            group_id = ?, gender = ?, birth_date = ?
        WHERE id = ?
        """
        
        execute_query(conn, query, (
            student.last_name,
            student.first_name,
            student.patronymic,
            student.group_id,
            student.gender,
            student.birth_date,
            student.id
        ))
        
        conn.close()
        return redirect(url_for('index'))
    
    # GET запрос - получение данных студента
    query = "SELECT * FROM students WHERE id = ?"
    student_data = execute_read_query(conn, query, (student_id,))
    
    if not student_data:
        conn.close()
        return "Студент не найден", 404
    
    student = Student.from_dict(student_data[0])
    groups = execute_read_query(conn, "SELECT * FROM groups ORDER BY group_number")
    
    conn.close()
    
    return render_template('student_form.html', 
                         student=student, 
                         groups=groups, 
                         action=url_for('edit_student', student_id=student_id))

# Удаление студента
@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = create_connection()
    
    # Сначала удаляем экзамены студента
    execute_query(conn, "DELETE FROM exams WHERE student_id = ?", (student_id,))
    
    # Затем удаляем студента
    execute_query(conn, "DELETE FROM students WHERE id = ?", (student_id,))
    
    conn.close()
    return redirect(url_for('index'))

# Список экзаменов студента
@app.route('/student/<int:student_id>/exams')
def student_exams(student_id):
    conn = create_connection()
    
    # Получение информации о студенте
    student_query = """
    SELECT s.*, g.group_number, g.specialization 
    FROM students s 
    JOIN groups g ON s.group_id = g.id 
    WHERE s.id = ?
    """
    student_data = execute_read_query(conn, student_query, (student_id,))
    
    if not student_data:
        conn.close()
        return "Студент не найден", 404
    
    student = Student.from_dict(student_data[0])
    student.group_number = student_data[0]['group_number']
    student.specialization = student_data[0]['specialization']
    
    # Получение экзаменов студента
    exams_query = """
    SELECT e.*, d.name as discipline_name 
    FROM exams e 
    JOIN disciplines d ON e.discipline_id = d.id 
    WHERE e.student_id = ? 
    ORDER BY e.exam_date DESC, e.year_of_study DESC, e.semester DESC
    """
    exams = execute_read_query(conn, exams_query, (student_id,))
    
    conn.close()
    
    return render_template('exam_list.html', 
                         student=student, 
                         exams=exams)

# Добавление экзамена
@app.route('/student/<int:student_id>/exam/add', methods=['GET', 'POST'])
def add_exam(student_id):
    conn = create_connection()
    
    if request.method == 'POST':
        exam = Exam.from_dict(request.form)
        exam.student_id = student_id
        
        query = """
        INSERT INTO exams (student_id, discipline_id, exam_date, grade, semester, year_of_study)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        execute_query(conn, query, (
            exam.student_id,
            exam.discipline_id,
            exam.exam_date,
            exam.grade,
            exam.semester,
            exam.year_of_study
        ))
        
        conn.close()
        return redirect(url_for('student_exams', student_id=student_id))
    
    # GET запрос - получение данных для формы
    # Получение информации о студенте
    student_query = """
    SELECT s.*, g.group_number, g.specialization, g.year_started 
    FROM students s 
    JOIN groups g ON s.group_id = g.id 
    WHERE s.id = ?
    """
    student_data = execute_read_query(conn, student_query, (student_id,))
    
    if not student_data:
        conn.close()
        return "Студент не найден", 404
    
    student = Student.from_dict(student_data[0])
    student.specialization = student_data[0]['specialization']
    student.year_started = student_data[0]['year_started']
    
    # Получение дисциплин, соответствующих направлению студента
    disciplines_query = """
    SELECT * FROM disciplines 
    WHERE specialization = ? 
    ORDER BY year_of_study, semester, name
    """
    disciplines = execute_read_query(conn, disciplines_query, (student.specialization,))
    
    # Получение доступных годов обучения (от 1 до максимального)
    current_year = datetime.now().year - student.year_started + 1
    available_years = list(range(1, min(current_year + 1, 6)))  # Максимум 6 курсов
    
    conn.close()
    
    return render_template('exam_form.html', 
                         exam=None, 
                         student=student, 
                         disciplines=disciplines,
                         available_years=available_years,
                         action=url_for('add_exam', student_id=student_id))

# Редактирование экзамена
@app.route('/exam/edit/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    conn = create_connection()
    
    if request.method == 'POST':
        exam = Exam.from_dict(request.form)
        exam.id = exam_id
        
        query = """
        UPDATE exams 
        SET discipline_id = ?, exam_date = ?, grade = ?, 
            semester = ?, year_of_study = ?
        WHERE id = ?
        """
        
        execute_query(conn, query, (
            exam.discipline_id,
            exam.exam_date,
            exam.grade,
            exam.semester,
            exam.year_of_study,
            exam.id
        ))
        
        # Получение student_id для редиректа
        student_query = "SELECT student_id FROM exams WHERE id = ?"
        student_data = execute_read_query(conn, student_query, (exam_id,))
        student_id = student_data[0]['student_id'] if student_data else None
        
        conn.close()
        
        if student_id:
            return redirect(url_for('student_exams', student_id=student_id))
        else:
            return redirect(url_for('index'))
    
    # GET запрос - получение данных экзамена
    exam_query = """
    SELECT e.*, d.name as discipline_name, d.specialization 
    FROM exams e 
    JOIN disciplines d ON e.discipline_id = d.id 
    WHERE e.id = ?
    """
    exam_data = execute_read_query(conn, exam_query, (exam_id,))
    
    if not exam_data:
        conn.close()
        return "Экзамен не найден", 404
    
    exam = Exam.from_dict(exam_data[0])
    exam.discipline_name = exam_data[0]['discipline_name']
    exam.specialization = exam_data[0]['specialization']
    
    # Получение информации о студенте
    student_query = "SELECT * FROM students WHERE id = ?"
    student_data = execute_read_query(conn, student_query, (exam.student_id,))
    
    if student_data:
        student = Student.from_dict(student_data[0])
    else:
        student = None
    
    # Получение дисциплин, соответствующих направлению
    disciplines_query = """
    SELECT * FROM disciplines 
    WHERE specialization = ? 
    ORDER BY year_of_study, semester, name
    """
    disciplines = execute_read_query(conn, disciplines_query, (exam.specialization,))
    
    available_years = list(range(1, 7))  # Все возможные годы
    
    conn.close()
    
    return render_template('exam_form.html', 
                         exam=exam, 
                         student=student, 
                         disciplines=disciplines,
                         available_years=available_years,
                         action=url_for('edit_exam', exam_id=exam_id))

# Удаление экзамена
@app.route('/exam/delete/<int:exam_id>', methods=['POST'])
def delete_exam(exam_id):
    conn = create_connection()
    
    # Получение student_id перед удалением
    student_query = "SELECT student_id FROM exams WHERE id = ?"
    student_data = execute_read_query(conn, student_query, (exam_id,))
    
    # Удаление экзамена
    execute_query(conn, "DELETE FROM exams WHERE id = ?", (exam_id,))
    
    conn.close()
    
    if student_data:
        return redirect(url_for('student_exams', student_id=student_data[0]['student_id']))
    else:
        return redirect(url_for('index'))

# API для получения дисциплин по году обучения
@app.route('/api/disciplines/<specialization>/<int:year_of_study>')
def get_disciplines_by_year(specialization, year_of_study):
    conn = create_connection()
    
    query = """
    SELECT * FROM disciplines 
    WHERE specialization = ? AND year_of_study = ?
    ORDER BY semester, name
    """
    
    disciplines = execute_read_query(conn, query, (specialization, year_of_study))
    conn.close()
    
    disciplines_list = [dict(d) for d in disciplines]
    return jsonify(disciplines_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)