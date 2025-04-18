import mysql.connector

def connect_database():
    connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'eggyisback0525',
            database = 'ssis_database'
    )
    return connection
        

    '''def fetch_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.cursor.fetchall()

    def insert_student(self, studentName, programCode):
        self.cursor.execute("INSERT INTO students (studentName, programCode) VALUES (%s, %s)", (studentName, programCode))
        self.conn.commit()

    def delete_student(self, studentID):
        self.cursor.execute("DELETE FROM students WHERE student_id = %s", (studentID,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
'''

