class Student:
    def __init__(self, id=None, last_name="", first_name="", patronymic="", group_id=None, gender="", birth_date=""):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.group_id = group_id
        self.gender = gender
        self.birth_date = birth_date
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            last_name=data.get('last_name', ''),
            first_name=data.get('first_name', ''),
            patronymic=data.get('patronymic', ''),
            group_id=data.get('group_id'),
            gender=data.get('gender', ''),
            birth_date=data.get('birth_date', '')
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'patronymic': self.patronymic,
            'group_id': self.group_id,
            'gender': self.gender,
            'birth_date': self.birth_date
        }

class Exam:
    def __init__(self, id=None, student_id=None, discipline_id=None, exam_date="", grade=0, semester=1, year_of_study=1):
        self.id = id
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.exam_date = exam_date
        self.grade = grade
        self.semester = semester
        self.year_of_study = year_of_study
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            student_id=data.get('student_id'),
            discipline_id=data.get('discipline_id'),
            exam_date=data.get('exam_date', ''),
            grade=data.get('grade', 0),
            semester=data.get('semester', 1),
            year_of_study=data.get('year_of_study', 1)
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'discipline_id': self.discipline_id,
            'exam_date': self.exam_date,
            'grade': self.grade,
            'semester': self.semester,
            'year_of_study': self.year_of_study
        }