from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QTableWidgetItem


class AggregateTab(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('tab_aggregate')

        self.label_data_section = QtWidgets.QLabel(self)
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))
        self.label_data_section.setText('Données')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(20, 40, 680, 400))
        self.table.setRowCount(20)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Critères', 'Couche', 'Champ', 'Pondération (0-1)'])

        self.table.setItem(0, 0, QTableWidgetItem('test'))
