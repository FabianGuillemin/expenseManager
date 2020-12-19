from qtpy import QtWidgets
from datetime import datetime


from ui.dialogincome import Ui_Dialog
from dbConnecter import DbConnector

class IncomeWindow(DbConnector, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Einnahme erfassen")

        if self.serverIsOn() == True:
            self.getIncomeCategories()
        else:
            self.msgDbCritical()

        self.ui.buttonBox.accepted.connect(self.writeDB)
        self.ui.dateEdit.setDate(datetime.now().date())

    def writeDB(self):
        y, m, d = self.ui.dateEdit.date().getDate()
        date = str(d) + "." + str(m) + "." + str(y)
        category = self.ui.comboBoxCategory.currentText()
        amount = self.ui.doubleSpinBoxAmount.value()
        cue = ""
        remark = self.ui.lineEditRemark.text()
        print(date, category, amount, remark)
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""INSERT INTO entries (entry_id, date, category, amount, cue, remark) VALUES (default, '{0}', '{1}', '{2}', '{3}', '{4}')""".format(date, category, amount, cue, remark))
            conn.commit()
        else:
            self.msgDbCritical()

    def getIncomeCategories(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM category WHERE in_or_outcome = 'Einnahme'")
            results = cur.fetchall()
            s = set()
            for result in results:
                s.add(result[1])
            self.ui.comboBoxCategory.addItems(s)
        else:
            self.msgDbCritical()










