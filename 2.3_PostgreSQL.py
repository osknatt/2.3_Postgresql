import psycopg2 as pg
from pprint import pprint

def create_db(): #создает таблицы
    cur.execute("""
        CREATE TABLE if not exists Student(
            id serial primary key,
            name varchar(100) not null,
            gpa numeric(10,2),
            birth timestamp with time zone);
    """)
    cur.execute("""
        CREATE TABLE if not exists Course(
            id serial primary key,
            name varchar(100) not null);
    """)
    cur.execute("""
           CREATE TABLE if not exists Student_Course(
               id serial primary key,
               student_id INTEGER REFERENCES Student(id),
               course_id INTEGER REFERENCES Course(id));
    """)

def delete_db(): #удаляет таблицы
    cur.execute("""DROP TABLE if exists Student CASCADE;""")
    cur.execute("""DROP TABLE if exists Course CASCADE;""")
    cur.execute("""DROP TABLE if exists Student_Course CASCADE;""")

def get_students(course_id): #возвращает студентов определенного курса
    # cur.execute(f"select * from Student where id={course_id}")
    cur.execute("""
                select s.id, s.name from Student_Course sc 
                join student s on s.id = sc.student_id 
                where sc.course_id = %s;
                """, (course_id, ))
    student_out = cur.fetchall()
    pprint(student_out)

def add_students(course_id, students): # создает студентов и записывает их на курс#
    for id in students:
        cur.execute("""
            insert into Student(name, gpa, birth)
            values (%s, %s, %s);
        """, students[id])
        cur.execute("""
            insert into Student_Course(student_id, course_id)
            values (%s, %s)
        """, (id, course_id))


def add_student(student): #просто создает студента
    for id in student:
        cur.execute("""
            insert into Student(name, gpa, birth)
            values (%s, %s, %s);
        """, student[id])

def add_courses(course): #создает курсы
    for id in course:
        cur.execute("""
            insert into Course(id, name)
            values (%s, %s);
        """, course[id])

def get_student(student_id): #возвращает студента по его id
    cur.execute("select * from student where id= %s", (student_id, ))
    student_out = cur.fetchall()
    pprint(student_out)

my_students = {
    '1': ('Vova', 4.28, '1980-04-04'),
    '2': ('Goga', 3.10, '1990-01-04'),
    '3': ('Gaga', 5.00, '1985-08-17')
}

my_courses = {
    '1': (1, 'Cooking'),
    '2': (2, 'Gardening'),
    '3': (3, 'Literature')
}


if __name__ == '__main__':
    with pg.connect(
            dbname='db',
            user='test_user',
            password='test'
    ) as conn:
        cur = conn.cursor()
        delete_db()
        create_db()
        add_student(my_students)
        get_student(1)
        add_courses(my_courses)
        add_students(2, my_students)
        get_students(2)