from typing import List, Union

from PySide2 import QtWidgets
from PySide2.QtWidgets import QTableWidgetItem


class MacbethScale(QtWidgets.QTableWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Level', 'Scale'])

        # Resize column to take all the horizontal space
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def set_values(self, levels_orders: List[int], levels: List[Union[str, int, float]], weights: List[float]):
        self.setRowCount(len(levels))

        for i, (order, level, weight) in enumerate(zip(levels_orders, levels, weights)):
            self.setItem(i, 0, QTableWidgetItem(str(order)))
            self.setItem(i, 1, QTableWidgetItem(str(level)))
            self.setItem(i, 2, QTableWidgetItem(str(weight)))

        self.resizeRowsToContents()
