from qtpy import QtWidgets
from datetime import datetime
from ui.dialogexpense import Ui_Dialog
from dbConnecter import DbConnector


class ExpenseWindow(DbConnector, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Ausgabe erfassen")

        if self.serverIsOn() == True:
            self.getExpenseCategories()
        else:
            self.msgDbCritical()

        self.ui.buttonBox.accepted.connect(self.writeDB)
        self.ui.dateEdit.setDate(datetime.now().date())

    def writeDB(self):
        y, m, d = self.ui.dateEdit.date().getDate()
        date = str(d) + "." + str(m) + "." + str(y)
        category = self.ui.comboBoxCategory.currentText()
        amount = self.ui.doubleSpinBoxAmount.value()
        #amount = value - value - value
        cue = self.ui.lineEditCue.text()
        remark = self.ui.lineEditRemark.text()

        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""INSERT INTO entries (entry_id, typ, date, category, amount, cue, remark) VALUES (default, 'Ausgabe', '{0}', '{1}', '{2}', '{3}', '{4}')""".format(date, category, amount, cue, remark))
            conn.commit()
        else:
            self.msgDbCritical()

    def getExpenseCategories(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM category WHERE in_or_outcome = 'Ausgabe'")
            results = cur.fetchall()
            s = set()
            for result in results:
                s.add(result[1])
            self.ui.comboBoxCategory.addItems(s)
        else:
            self.msgDbCritical()










