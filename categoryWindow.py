from qtpy import QtWidgets

from ui.dialogcategories import Ui_Dialog
from dbConnecter import DbConnector

#TODO Bearbeiten und Löschen noch umsetzen

class CategoryWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Kategorien bearbeiten")
        self.fillTableWidgetCat()

        self.ui.btnSave.clicked.connect(self.writeDB)

    def writeDB(self):
        category = self.ui.lineEditCategory.text()
        typ = self.ui.comboBoxInOrOutcome.currentText()

        conn = DbConnector().connect()
        cur = conn.cursor()
        cur.execute("""INSERT INTO category (category_id, category, in_or_outcome) VALUES (default, '{0}', '{1}')""".format(category, typ))
        conn.commit()

        self.ui.lineEditCategory.clear()
        self.fillTableWidgetCat()

    def fillTableWidgetCat(self):
        conn = DbConnector().connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM category")
        result = cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for rowNumber, rowData in enumerate(result):
            self.ui.tableWidget.insertRow(rowNumber)
            self.ui.tableWidget.setItem(rowNumber, 0, QtWidgets.QTableWidgetItem(str(rowData[1])))
            self.ui.tableWidget.setItem(rowNumber, 1, QtWidgets.QTableWidgetItem(str(rowData[2])))












