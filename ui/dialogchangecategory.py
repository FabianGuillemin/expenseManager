# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\dialogchangecategory.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEditId = QtWidgets.QLineEdit(Dialog)
        self.lineEditId.setReadOnly(True)
        self.lineEditId.setObjectName("lineEditId")
        self.gridLayout.addWidget(self.lineEditId, 0, 1, 1, 1)
        self.lineEditCategory = QtWidgets.QLineEdit(Dialog)
        self.lineEditCategory.setObjectName("lineEditCategory")
        self.gridLayout.addWidget(self.lineEditCategory, 1, 1, 1, 1)
        self.comboBoxTyp = QtWidgets.QComboBox(Dialog)
        self.comboBoxTyp.setObjectName("comboBoxTyp")
        self.comboBoxTyp.addItem("")
        self.comboBoxTyp.addItem("")
        self.gridLayout.addWidget(self.comboBoxTyp, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSave = QtWidgets.QPushButton(Dialog)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.btnDelete = QtWidgets.QPushButton(Dialog)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout.addWidget(self.btnDelete)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ID"))
        self.label_2.setText(_translate("Dialog", "Kategorie"))
        self.label_3.setText(_translate("Dialog", "Typ"))
        self.comboBoxTyp.setItemText(0, _translate("Dialog", "Ausgabe"))
        self.comboBoxTyp.setItemText(1, _translate("Dialog", "Einnahme"))
        self.btnSave.setText(_translate("Dialog", "Änderung speichern"))
        self.btnDelete.setText(_translate("Dialog", "Löschen"))
