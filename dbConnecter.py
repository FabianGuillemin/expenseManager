import psycopg2
import socket
from qtpy import QtWidgets

class DbConnector():

    def connect(self):
        if self.serverIsOn() == True:
            self.conn = psycopg2.connect("host=192.168.1.213 user=admin password=admin dbname=db_expensemanager")
            print(self.conn)
            return self.conn
        else:
            print("Verbindung nicht möglich")

    def serverIsOn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(("192.168.1.213", 5432))
        s.close()
        if result == 0:
            return True
        else:
            return False

    def dbClose(self):
        print("DB close")
        self.conn.close()

    def msgDbCritical(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText("Verbindung zu der Datenbank nicht möglich. Bitte Verbindung oder Konfigurationen prüfen.")
        self.msg.setWindowTitle("Fehler")
        self.msg.show()

