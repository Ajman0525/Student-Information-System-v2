import pymysql

class DatabaseManager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "eggyisback0525"
        self.database = "ssis_database"
        self.cursor = None

    def connect_database(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
