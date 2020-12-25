from qtpy import QtWidgets
from ui.dialogchangeentry import Ui_Dialog
from dbConnecter import DbConnector


class ChangeEntryWindow(DbConnector, QtWidgets.QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.id = id

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Eintrag bearbeiten")
        self.changeEntry(self.id)
        self.ui.btn_delete.clicked.connect(self.deleteEntry)
        self.ui.btn_save.clicked.connect(self.updateEntry)

    def changeEntry(self, id):
        conn = DbConnector().connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries where entry_id = '{0}'".format(id))
        results = cur.fetchall()
        for item in results:
            entry_id, date, category, amount, cue, remark, typ = item
        self.ui.dateEdit.setDate(date)
        self.ui.lineEditCue.setText(cue)
        self.ui.lineEditRemark.setText(remark)
        self.ui.doubleSpinBoxAmount.setValue(float(amount))
        if typ == "Ausgabe":
            self.getExpenseCategories()
            self.ui.comboBoxCategory.setCurrentText(category)
        else:
            self.getIncomeCategories()
            self.ui.comboBoxCategory.setCurrentText(category)


    def getExpenseCategories(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM category WHERE typ = 'Ausgabe'")
            results = cur.fetchall()
            s = set()
            for result in results:
                s.add(result[1])
            self.ui.comboBoxCategory.addItems(s)
        else:
            self.msgDbCritical()

    def getIncomeCategories(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM category WHERE typ = 'Einnahme'")
            results = cur.fetchall()
            s = set()
            for result in results:
                s.add(result[1])
            self.ui.comboBoxCategory.addItems(s)
        else:
            self.msgDbCritical()

    def windowClose(self):
        self.close()

    def deleteEntry(self):
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""DELETE FROM entries where entry_id = '{0}'""".format(self.id))
            conn.commit()
            self.windowClose()
        else:
            self.msgDbCritical()

    def updateEntry(self):
        y, m, d = self.ui.dateEdit.date().getDate()
        date = str(d) + "." + str(m) + "." + str(y)
        category = self.ui.comboBoxCategory.currentText()
        amount = self.ui.doubleSpinBoxAmount.value()
        cue = self.ui.lineEditCue.text()
        remark = self.ui.lineEditRemark.text()
        if self.serverIsOn() == True:
            conn = DbConnector().connect()
            cur = conn.cursor()
            cur.execute("""UPDATE entries SET date = '{0}', category = '{1}', amount = '{2}', cue = '{3}', remark = '{4}' WHERE entry_id = '{5}'""".format(date, category, amount, cue, remark, self.id))
            conn.commit()
            self.windowClose()
        else:
            self.msgDbCritical()
















