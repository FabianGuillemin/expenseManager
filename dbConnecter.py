import psycopg2
import socket
import csv
from qtpy import QtWidgets
from ui.dialogdbconfiguration import Ui_Dialog


class DbConnector():

    def connect(self):
        dict = self.readConfFile()
        host = dict.get("host")
        user = dict.get("user")
        pw = dict.get("pw")
        db_name = dict.get("db_name")
        if self.serverIsOn() == True:
            if self.checkLogin() == True:
                self.conn = psycopg2.connect("host='{0}' user='{1}' password='{2}' dbname='{3}'".format(host, user, pw, db_name))
                return self.conn
        else:
            print("Verbindung nicht möglich")

    def serverIsOn(self):
        dict = self.readConfFile()
        host = dict.get("host")
        port = dict.get("port")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, int(port)))
        s.close()
        if result == 0:
            return True
        else:
            return False

    def checkLogin(self):
        dict = self.readConfFile()
        host = dict.get("host")
        user = dict.get("user")
        pw = dict.get("pw")
        db_name = dict.get("db_name")
        try:
            psycopg2.connect("host='{0}' user='{1}' password='{2}' dbname='{3}'".format(host, user, pw, db_name))
            return True
        except psycopg2.OperationalError:
            print("psycopg2.OperationalError")
            return False

    def dbClose(self):
        print("DB close")
        self.conn.close()

    def readConfFile(self):
        dictConfValues = {}
        with open("dbConfFile.txt", "r", newline='', encoding="UTF-8") as file:
            for line in file:
                values = line.strip().split(";")
                dictConfValues[values[0]] = values[1]
        return dictConfValues

    def msgDbCritical(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText("Verbindung zu der Datenbank nicht möglich. Bitte Verbindung oder Konfigurationen prüfen.")
        self.msg.setWindowTitle("Fehler")
        self.msg.show()

    def msgLoginCritical(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText("Logindaten stimmen nicht")
        self.msg.setWindowTitle("Fehler")
        self.msg.show()


class DbConfiguration(DbConnector, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Datenbank Konfiguration")
        dict = self.readConfFile()
        self.ui.lineEditHost.setText(dict["host"])
        self.ui.spinBoxPort.setValue(int(dict["port"]))
        self.ui.lineEditUser.setText(dict["user"])
        self.ui.lineEditPW.setText(dict["pw"])
        self.ui.lineEditDBName.setText(dict["db_name"])

        self.ui.buttonBox.accepted.connect(self.writeConfFile)

    def writeConfFile(self):
        dictConfValues = {
            "host": self.ui.lineEditHost.text().strip(),
            "port": self.ui.spinBoxPort.text().strip(),
            "user": self.ui.lineEditUser.text().strip(),
            "pw": self.ui.lineEditPW.text().strip(),
            "db_name": self.ui.lineEditDBName.text().strip()
        }
        with open("dbConfFile.txt", "w", newline='', encoding="UTF-8") as csvfile:
            file = csv.writer(csvfile, delimiter=';')
            for line in dictConfValues.items():
                file.writerow(line)


