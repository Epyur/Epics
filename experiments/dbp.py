import sqlite3


def init_many_to_many_db():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

    # Таблица студентов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Таблица курсов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
    ''')

    # Промежуточная таблица для связи многие-ко-многим
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_courses (
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    ''')

    conn.commit()
    conn.close()


# Пример использования
init_many_to_many_db()

conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Добавляем студентов
students = [("Иван Иванов",), ("Петр Петров",)]
cursor.executemany("INSERT INTO students (name) VALUES (?)", students)

# Добавляем курсы
courses = [("Математика",), ("Физика",)]
cursor.executemany("INSERT INTO courses (title) VALUES (?)", courses)

# Связываем студентов с курсами
# Иван изучает Математику и Физику, Петр - только Математику
enrollments = [(1, 1), (1, 2), (2, 1)]
cursor.executemany("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", enrollments)

conn.commit()
conn.close()