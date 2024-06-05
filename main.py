import random

import faker
from faker.providers import DynamicProvider
import psycopg2
import datetime


class DBConnection:
    connection = None
    cursor = None

    def __init__(self, conn_str):
        try:
            self.connection = psycopg2.connect(conn_str)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(e)

    def exec_cursor(self, sql_text, data=None):
        try:
            if type(data) is list:
                self.cursor.executemany(sql_text, data)
            elif not data:
                self.cursor.execute(sql_text)
            else:
                self.cursor.execute(sql_text, data)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)


class FakeDataGenerator:
    students = []
    teachers = []
    subjects = []
    fk = None
    marks_qty = 0
    subject_list = ['Mathematics', 'Algebra', 'Geometry', 'Science', 'Geography', 'History', 'English', 'Spanish',
                    'German', 'French', 'Latin', 'Greek', 'Arabic', 'Computer Science', 'Art', 'Economics', 'Music',
                    'Drama', 'Physical Education']
    db_conn = None

    def __init__(self, students_qty, teachers_qty, subjects_qty, marks_qty=20):
        self.fk = faker.Faker()
        self.fk.add_provider(DynamicProvider(provider_name="subject", elements=self.subject_list))
        self.subjects = self.gen_subjects(subjects_qty)
        self.teachers = self.gen_names(teachers_qty)
        self.students = self.gen_names(students_qty)
        self.marks_qty = marks_qty

    def set_db_connection(self, db_conn: DBConnection):
        self.db_conn = db_conn

    def gen_subjects(self, subjects_qty):
        res = set()
        while len(res) < subjects_qty:
            res.add(self.fk.subject())
        return list(res)

    def fill_db_with_fake_data(self):
        self.fill_db_group_with_fake_data()
        self.fill_db_students_with_fake_data()
        self.fill_db_teachers_with_fake_data()
        self.fill_db_subjects_with_fake_data()
        self.fill_db_marks_with_fake_data()

    def fill_db_group_with_fake_data(self):
        sql = "INSERT INTO hw6.groups (group_name) values(%s); COMMIT;"
        self.db_conn.exec_cursor(sql, self.records_groups())

    def fill_db_students_with_fake_data(self):
        sql = "INSERT INTO hw6.students (full_name, group_id) values(%s, %s); COMMIT;"
        self.db_conn.exec_cursor(sql, self.records_students())

    def fill_db_teachers_with_fake_data(self):
        sql = "INSERT INTO hw6.teachers (full_name) values(%s); COMMIT;"
        self.db_conn.exec_cursor(sql, self.records_teacher())

    def fill_db_subjects_with_fake_data(self):
        sql = "INSERT INTO hw6.subjects (subject_name, teacher_id) values(%s, %s); COMMIT;"
        self.db_conn.exec_cursor(sql, self.records_subjects())

    def fill_db_marks_with_fake_data(self):
        sql = "INSERT INTO hw6.marks (student_id, subject_id, mark, timestamp) values(%s, %s, %s, %s); COMMIT;"
        self.db_conn.exec_cursor(sql, self.records_marks())

    def records_subjects(self):
        teach_ids = self.db_conn.exec_cursor("select id from hw6.teachers")
        teach_ids = [el[0] for el in teach_ids]
        ret = []
        for subj in self.subjects:
            ret.append((subj, random.choice(teach_ids)))
        return ret

    def records_groups(self):
        ret = []
        for group in range(1, 4):
            ret.append((f"group_{group}",))
        return ret

    def records_teacher(self):
        ret = []
        for teacher in self.teachers:
            ret.append((teacher,))
        return ret

    def records_students(self):
        group_ids = self.db_conn.exec_cursor("select id from hw6.groups")
        group_ids = [el[0] for el in group_ids]
        ret = []
        for student in self.students:
            ret.append((student, random.choice(group_ids)))
        return ret

    def records_marks(self):
        students_ids = self.db_conn.exec_cursor("select id from hw6.students")
        students_ids = [el[0] for el in students_ids]
        subj_ids = self.db_conn.exec_cursor("select id from hw6.subjects")
        subj_ids = [el[0] for el in subj_ids]
        ret = []
        for s_id in students_ids:
            for _ in range(1, self.marks_qty + 1):
                ts = datetime.datetime(2024, random.randrange(1, 12),
                                       random.randrange(1, 28),
                                       random.randrange(1, 24),
                                       random.randrange(1, 60),
                                       random.randrange(1, 60))
                ret.append((s_id, random.choice(subj_ids), random.randrange(1, 100), ts))
        return ret

    def gen_names(self, qty: int) -> list:
        return [self.fk.name() for _ in range(1, qty + 1)]


if __name__ == "__main__":
    fk = FakeDataGenerator(50, 5, 8)
    with open("db_conn_set.ini", "r", encoding="utf-8") as f:
        db_conn_set = f.read()
        db_conn_set = db_conn_set.replace(",\n", "").strip()
    with open("create_DB.sql", "r", encoding="utf-8") as f:
        sql = f.read()
        sql = sql.replace("\n", " ")
    with DBConnection(db_conn_set) as db:
        db.exec_cursor(sql)  # create schema and tables
        fk.set_db_connection(db)
        fk.fill_db_with_fake_data()

        # with open("sql_queries/1.sql", "r", encoding="utf-8") as f:
        #     query = f.read()
        #     query = query.replace(",\n", "").strip()
        # print(db.exec_cursor(query))

