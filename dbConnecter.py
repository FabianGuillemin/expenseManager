import psycopg2

class DbConnector():

    def connect(self):
        self.conn = psycopg2.connect("host=192.168.1.213 user=admin password=admin dbname=db_expensemanager")
        return self.conn

    def close(self):
        print("DB close")
        self.conn.close()

