from typing import Dict

from PySide2 import QtWidgets, QtCore


class CriterionRemover(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.resize(800, 260)

        self.label_layer_to_select = QtWidgets.QLabel(self, text='Select the layer to remove')
        self.label_layer_to_select.setGeometry(QtCore.QRect(20, 100, 311, 19))

        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.setGeometry(QtCore.QRect(20, 120, 731, 31))

        self.btn_remove_criterion = QtWidgets.QPushButton(self, text='Remove criterion', clicked=self.remove_criterion)
        self.btn_remove_criterion.setGeometry(QtCore.QRect(610, 210, 151, 31))

        self.criteria: Dict[str, int] = {}

        for index in range(self.parent().table.rowCount()):
            filepath = self.parent().table.item(index, 0).text()
            layer = self.parent().table.item(index, 1).text()
            criterion = self.parent().table.item(index, 2).text()

            self.criteria[f'{filepath} | {layer} | {criterion}'] = index

        self.combobox.addItems(self.criteria.keys())

    def remove_criterion(self):
        criterion = self.combobox.currentText()
        row_index = self.criteria[criterion]

        self.parent().table.removeRow(row_index)

        self.accept()
