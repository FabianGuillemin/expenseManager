from qtpy import QtWidgets
from ui.dialogcategories import Ui_Dialog
from ui.dialogchangecategory import Ui_Dialog as Ui_DialogChange
from dbConnecter import DbConnector


class CategoryWindow(DbConnector, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Kategorien bearbeiten")

        if self.serverIsOn() == True:
            self.fillTableWidgetCat()
        else:
            self.msgDbCritical()

        self.ui.btnSave.clicked.connect(self.writeDB)
        self.ui.btnUpdate.clicked.connect(self.fillTableWidgetCat)
        self.ui.tableWidget.cellDoubleClicked.connect(self.clickRow)

    def clickRow(self, row):
        id = str(self.ui.tableWidget.item(row, 0).text())
        self.ChangeCategoryWindow = ChangeCategoryWindow(id)
        self.ChangeCategoryWindow.show()

    def writeDB(self):
        category = self.ui.lineEditCategory.text()
        typ = self.ui.comboBoxInOrOutcome.currentText()
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""INSERT INTO category (category_id, category, in_or_outcome) VALUES (default, '{0}', '{1}')""".format(category, typ))
            conn.commit()
        else:
            self.msgDbCritical()

        self.ui.lineEditCategory.clear()
        self.fillTableWidgetCat()

    def fillTableWidgetCat(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM category ORDER BY category_id ASC")
            result = cur.fetchall()
            self.ui.tableWidget.setRowCount(0)
            for rowNumber, rowData in enumerate(result):
                self.ui.tableWidget.insertRow(rowNumber)
                self.ui.tableWidget.setItem(rowNumber, 0, QtWidgets.QTableWidgetItem(str(rowData[0])))
                self.ui.tableWidget.setItem(rowNumber, 1, QtWidgets.QTableWidgetItem(str(rowData[1])))
                self.ui.tableWidget.setItem(rowNumber, 2, QtWidgets.QTableWidgetItem(str(rowData[2])))
        else:
            self.msgDbCritical()


class ChangeCategoryWindow(DbConnector, QtWidgets.QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.id = id

        self.uic = Ui_DialogChange()
        self.uic.setupUi(self)
        self.setWindowTitle("Kategorie bearbeiten")

        self.changeCategory(id)

        self.uic.btnDelete.clicked.connect(self.deleteCategory)
        self.uic.btnSave.clicked.connect(self.updateCategory)

    def windowClose(self):
        self.close()

    def deleteCategory(self):
        id = self.uic.lineEditId.text()
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""DELETE FROM category where category_id = '{0}'""".format(id))
            conn.commit()
            self.windowClose()
        else:
            self.msgDbCritical()

    def updateCategory(self):
        category = self.uic.lineEditCategory.text()
        typ = self.uic.comboBoxTyp.currentText()
        id = self.uic.lineEditId.text()
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""UPDATE category SET category = '{0}', in_or_outcome = '{1}' WHERE category_id = '{2}'""".format(category, typ, id))
            conn.commit()
            self.windowClose()
        else:
            self.msgDbCritical()

    def changeCategory(self, id):
        conn = DbConnector().connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM category where category_id = '{0}'".format(id))
        results = cur.fetchall()
        for item in results:
            id, category, typ = item
        self.uic.lineEditId.setText(str(id))
        self.uic.lineEditCategory.setText(str(category))
        if str(typ) == "Ausgabe":
            self.uic.comboBoxTyp.setCurrentIndex(0)
        else:
            self.uic.comboBoxTyp.setCurrentIndex(1)












