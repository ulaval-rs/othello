from PySide2 import QtWidgets, QtCore

from othello.ui.criterion_wizard import CriterionWizard


class AggregateTab(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('tab_aggregate')

        self.label_data_section = QtWidgets.QLabel(self, text='Data')
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))

        self.btn_add_criterion = QtWidgets.QPushButton(self, text='Add criterion', clicked=self.add_criterion)
        self.btn_add_criterion.setGeometry(QtCore.QRect(20, 40, 100, 31))

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(20, 80, 731, 260))
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Criterion', 'Layer', 'Field', 'Weight [0-1]'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def add_criterion(self):
        wizard = CriterionWizard(self)
        wizard.show()

        return
