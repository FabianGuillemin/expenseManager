import sys
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow
from dbConnecter import DbConnector, DbConfiguration
from expenseWindow import ExpenseWindow
from incomeWindow import IncomeWindow
from categoryWindow import CategoryWindow
from changeEntryWindow import ChangeEntryWindow

app = QtWidgets.QApplication(sys.argv)


class MainWindow(DbConnector, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("expense Manager - BETA")

        if self.serverIsOn() == True:
            if self.checkLogin() == True:
                self.fillTableWidget()
            else:
                self.msgLoginCritical()
        else:
            self.msgDbCritical()

        self.ui.btnExpense.clicked.connect(self.addExpense)
        self.ui.btnIncome.clicked.connect(self.addIncome)
        self.ui.btnUpdate.clicked.connect(self.fillTableWidget)
        self.ui.actionKategorie_bearbeiten.triggered.connect(self.confCategory)
        self.ui.actionDB_Konfiguration.triggered.connect(self.confDb)
        self.ui.tableWidget.cellDoubleClicked.connect(self.clickRow)

    def clickRow(self, row):
        id = str(self.ui.tableWidget.item(row, 0).text())
        self.ChangeEntryWindow = ChangeEntryWindow(id)
        self.ChangeEntryWindow.show()

    def addExpense(self):
        self.expenseWindow = ExpenseWindow()
        self.expenseWindow.show()

    def addIncome(self):
        self.incomeWindow = IncomeWindow()
        self.incomeWindow.show()

    def confCategory(self):
        self.categoryWindow = CategoryWindow()
        self.categoryWindow.show()

    def confDb(self):
        self.dbConfWindow = DbConfiguration()
        self.dbConfWindow.show()

    def fillTableWidget(self):
        conn = DbConnector().connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries ORDER BY entry_id DESC LIMIT 40")
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


window = MainWindow()
window.show()

sys.exit(app.exec_())
