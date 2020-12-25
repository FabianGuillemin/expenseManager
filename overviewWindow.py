from qtpy import QtWidgets
from datetime import datetime
from ui.mainwindowoverview import Ui_MainWindow
from changeEntryWindow import ChangeEntryWindow
from dbConnecter import DbConnector


class OverviewWindow(DbConnector, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        y, m, d = str(datetime.now().date()).split("-")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Buchungsübersicht")

        self.ui.comboBoxMonth.addItems(self.setMonth())
        self.ui.comboBoxMonth.setCurrentText(str(m))
        self.ui.comboBoxYear.addItems(self.setYear())
        self.ui.comboBoxYear.setCurrentText(str(y))

        if self.serverIsOn() == True:
            if self.checkLogin() == True:
                self.fillTableWidget()
            else:
                self.msgLoginCritical()
        else:
            self.msgDbCritical()

        self.ui.btnFilter.clicked.connect(self.fillTableWidget)
        self.ui.tableWidget.cellDoubleClicked.connect(self.clickRow)

    def clickRow(self, row):
        id = str(self.ui.tableWidget.item(row, 0).text())
        self.ChangeEntryWindow = ChangeEntryWindow(id)
        self.ChangeEntryWindow.show()

    def setMonth(self):
        sMonth = {"*", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"}
        return sorted(sMonth)

    def setYear(self):
        sYear = set()
        y, m, d = str(datetime.now().date()).split("-")
        year = int(y) - 3
        for i in range(0, 10):
            y = year + i
            sYear.add(str(y))
        sYear.add("*")
        return sorted(sYear)

    def fillTableWidget(self):
        conn = DbConnector().connect()
        cur = conn.cursor()
        month = self.ui.comboBoxMonth.currentText()
        year = self.ui.comboBoxYear.currentText()
        if month == "*" and year == "*":
            cur.execute("SELECT * FROM entries ORDER BY date DESC")
        elif month == "*" and year != "*":
            cur.execute("SELECT * FROM entries WHERE date_part('year', date::date) = '{0}' ORDER BY date DESC".format(year))
        else:
            cur.execute("SELECT * FROM entries WHERE date_part('month', date::date) = '{0}' AND date_part('year', date::date) = '{1}' ORDER BY date DESC".format(month, year))
        result = cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for rowNumber, rowData in enumerate(result):
            self.ui.tableWidget.insertRow(rowNumber)
            date = str(rowData[1].strftime("%d.%m.%Y"))
            self.ui.tableWidget.setItem(rowNumber, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
            self.ui.tableWidget.setItem(rowNumber, 4, QtWidgets.QTableWidgetItem(str(rowData[6])))
            self.ui.tableWidget.setItem(rowNumber, 1, QtWidgets.QTableWidgetItem(str(date)))
            self.ui.tableWidget.setItem(rowNumber, 2, QtWidgets.QTableWidgetItem(str(rowData[2])))
            self.ui.tableWidget.setItem(rowNumber, 3, QtWidgets.QTableWidgetItem(str(rowData[3])))
            self.ui.tableWidget.setItem(rowNumber, 5, QtWidgets.QTableWidgetItem(str(rowData[4])))
            self.ui.tableWidget.setItem(rowNumber, 6, QtWidgets.QTableWidgetItem(str(rowData[5])))
        self.ui.tableWidget.setColumnHidden(0, True)
        #TODO month != "*" and year == "*" noch abfangen
        if month == "*" and year == "*":
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Ausgabe'")
        elif month == "*" and year != "*":
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Ausgabe' AND date_part('year', date::date) = '{0}'".format(year))
        else:
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Ausgabe' AND date_part('month', date::date) = '{0}' AND date_part('year', date::date) = '{1}'".format(month, year))
        resultExpense = cur.fetchall()
        expense = resultExpense[0][0]
        if expense == None:
            expense = 0
        self.ui.totalExpense.setText(str(expense))
        if month == "*" and year == "*":
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Einnahme'")
        elif month == "*" and year != "*":
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Einnahme' AND date_part('year', date::date) = '{0}'".format(year))
        else:
            cur.execute("SELECT SUM(amount) FROM entries WHERE typ = 'Einnahme' AND date_part('month', date::date) = '{0}' AND date_part('year', date::date) = '{1}'".format(month, year))
        resultReceipt = cur.fetchall()
        receipt = resultReceipt[0][0]
        if receipt == None:
            receipt = 0
        self.ui.totalReceipt.setText(str(receipt))
        diff = receipt - expense
        self.ui.totalDiff.setText(str(diff))
        self.ui.totalEntries.setText(str(self.ui.tableWidget.rowCount()))


